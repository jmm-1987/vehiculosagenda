"""Documento electrónico de control administrativo (DeCA)."""
from __future__ import annotations

import os
import re
import secrets
import time
from datetime import datetime, date

from flask import render_template, redirect, url_for, request, send_file
from flask_login import login_required, current_user

import db
from deca.nif import nif_valido, normalizar_nif
from deca.pdf_deca import generar_pdf_deca
from models import (
    DecaCambio,
    DecaConductor,
    DecaContratante,
    DecaDocumento,
    DecaEnvio,
    DecaLugar,
    DecaTransportista,
    DecaVehiculoCat,
)

REPO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "deca_repositorio")
_TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{12,80}$")

CATALOGOS = {
    "transportista": {
        "titulo": "Transportistas",
        "ayuda": "Transportista efectivo. La norma exige nombre o razón social y NIF.",
        "model": DecaTransportista,
        "orden": "nombre",
        "campos": [
            ("nombre", "Nombre o razón social", True),
            ("nif", "NIF", True),
            ("domicilio", "Domicilio", False),
            ("telefono", "Teléfono", False),
        ],
    },
    "contratante": {
        "titulo": "Contratantes del servicio",
        "ayuda": "Cargador contractual. La norma exige nombre o razón social, NIF y domicilio.",
        "model": DecaContratante,
        "orden": "nombre",
        "campos": [
            ("nombre", "Nombre o razón social", True),
            ("nif", "NIF", True),
            ("domicilio", "Domicilio", True),
            ("telefono", "Teléfono", False),
        ],
    },
    "conductor": {
        "titulo": "Conductores",
        "ayuda": "Se guarda el nombre. El NIF o DNI es voluntario, pero si se indica tiene que ser válido.",
        "model": DecaConductor,
        "orden": "nombre",
        "campos": [
            ("nombre", "Nombre", True),
            ("nif", "NIF o DNI", False),
            ("telefono", "Teléfono", False),
        ],
    },
    "vehiculo": {
        "titulo": "Vehículos",
        "ayuda": "Matrícula del vehículo motor y, si viaja, la del remolque o semirremolque.",
        "model": DecaVehiculoCat,
        "orden": "matricula",
        "campos": [
            ("matricula", "Matrícula", True),
            ("matricula_remolque", "Matrícula del remolque", False),
            ("descripcion", "Descripción", False),
        ],
    },
    "origen": {
        "titulo": "Orígenes",
        "ayuda": "Lugar de origen del envío.",
        "model": DecaLugar,
        "orden": "lugar",
        "tipo_lugar": "origen",
        "campos": [
            ("lugar", "Lugar", True),
            ("direccion", "Dirección", False),
            ("cp", "Código postal", False),
            ("poblacion", "Población", False),
            ("provincia", "Provincia", False),
        ],
    },
    "destino": {
        "titulo": "Destinos",
        "ayuda": "Lugar de destino del envío.",
        "model": DecaLugar,
        "orden": "lugar",
        "tipo_lugar": "destino",
        "campos": [
            ("lugar", "Lugar", True),
            ("direccion", "Dirección", False),
            ("cp", "Código postal", False),
            ("poblacion", "Población", False),
            ("provincia", "Provincia", False),
        ],
    },
}


class DecaError(Exception):
    def __init__(self, mensajes):
        if isinstance(mensajes, str):
            mensajes = [mensajes]
        self.mensajes = list(mensajes)
        super().__init__(" ".join(self.mensajes))


def _usuario() -> str:
    if current_user and getattr(current_user, "is_authenticated", False):
        return current_user.username or ""
    return ""


def _id(valor) -> int | None:
    valor = (valor or "").strip()
    if valor.isdigit():
        return int(valor)
    return None


def _limpiar(valor) -> str:
    return " ".join((valor or "").replace("\r", " ").split())


def _mayus(valor) -> str:
    return _limpiar(valor).upper()


def formato_peso(numero: float) -> str:
    if abs(numero - round(numero)) < 1e-9:
        return f"{int(round(numero)):,}".replace(",", ".")
    texto = f"{numero:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")
    while texto.endswith("0"):
        texto = texto[:-1]
    return texto.rstrip(",")


def parse_peso(valor: str) -> float:
    texto = (valor or "").strip().lower().replace("kg", "").replace(" ", "")
    if not texto:
        raise ValueError
    if "," in texto and "." in texto:
        if texto.rfind(",") > texto.rfind("."):
            texto = texto.replace(".", "").replace(",", ".")
        else:
            texto = texto.replace(",", "")
    elif "," in texto:
        texto = texto.replace(",", ".")
    numero = float(texto)
    if numero <= 0 or numero > 1_000_000:
        raise ValueError
    return numero


def lugar_texto(lugar, direccion="", cp="", poblacion="", provincia="") -> str:
    partes = []
    if _limpiar(lugar):
        partes.append(_limpiar(lugar))
    if _limpiar(direccion):
        partes.append(_limpiar(direccion))
    localidad = " ".join(p for p in [_limpiar(cp), _limpiar(poblacion)] if p)
    if localidad:
        partes.append(localidad)
    if _limpiar(provincia) and _limpiar(provincia).lower() not in _limpiar(poblacion).lower():
        partes.append(_limpiar(provincia))
    return " / ".join(partes)


def _url_publica(token: str) -> str:
    base = os.environ.get("DECA_PUBLIC_BASE_URL", "").strip().rstrip("/")
    if not base:
        proto = (request.headers.get("X-Forwarded-Proto") or request.scheme or "https").split(",")[0].strip()
        host = (request.headers.get("X-Forwarded-Host") or request.host).split(",")[0].strip()
        base = f"{proto}://{host}"
    return f"{base}/deca/d/{token}"


def _ruta_pdf(token: str) -> str:
    return os.path.join(REPO_DIR, f"{token}.pdf")


def _escribir_pdf(token: str, contenido: bytes) -> None:
    os.makedirs(REPO_DIR, exist_ok=True)
    destino = _ruta_pdf(token)
    temporal = destino + ".tmp"
    with open(temporal, "wb") as fichero:
        fichero.write(contenido)
    ultimo_error = None
    for _ in range(4):
        try:
            os.replace(temporal, destino)
            return
        except PermissionError as exc:
            ultimo_error = exc
            time.sleep(0.15)
    try:
        with open(destino, "r+b") as fichero:
            fichero.seek(0)
            fichero.write(contenido)
            fichero.truncate()
        os.remove(temporal)
        return
    except OSError:
        pass
    raise DecaError(
        "No se ha podido actualizar el PDF porque el archivo está abierto. Ciérralo y vuelve a guardar."
    ) from ultimo_error


def _siguiente_numero(momento: datetime) -> str:
    prefijo = f"DECA-{momento.year}-"
    filas = db.session.query(DecaDocumento.numero).filter(DecaDocumento.numero.like(prefijo + "%")).all()
    maximo = 0
    for (numero,) in filas:
        try:
            maximo = max(maximo, int(str(numero).split("-")[-1]))
        except ValueError:
            continue
    return f"{prefijo}{maximo + 1:04d}"


def _fmt_fecha(valor: date | None) -> str:
    if not valor:
        return ""
    return valor.strftime("%d/%m/%Y")


def _fmt_dt(valor: datetime | None) -> str:
    if not valor:
        return ""
    return valor.strftime("%d/%m/%Y %H:%M:%S")


def _resumen(doc: DecaDocumento, envios: list) -> str:
    lineas = [
        f"Contratante: {doc.contratante_nombre} | NIF {doc.contratante_nif} | {doc.contratante_domicilio}",
        f"Transportista: {doc.transportista_nombre} | NIF {doc.transportista_nif}",
        f"Conductor: {doc.conductor_nombre}" + (f" | NIF {doc.conductor_nif}" if doc.conductor_nif else ""),
        f"Vehículo: {doc.vehiculo_matricula}" + (f" / remolque {doc.vehiculo_remolque}" if doc.vehiculo_remolque else ""),
        f"Fecha de realización: {_fmt_fecha(doc.fecha_realizacion)}",
        f"Autorización especial: {doc.autorizacion_especial or 'No consta'}",
        f"Observaciones: {doc.observaciones or 'Sin observaciones'}",
        "Envíos:",
    ]
    for envio in envios:
        lineas.append(
            f"{envio.orden}. {lugar_texto(envio.origen_lugar, envio.origen_direccion, envio.origen_cp, envio.origen_poblacion, envio.origen_provincia)}"
            f" -> {lugar_texto(envio.destino_lugar, envio.destino_direccion, envio.destino_cp, envio.destino_poblacion, envio.destino_provincia)}"
            f" | {envio.naturaleza} | {envio.peso} kg"
        )
    return "\n".join(lineas)


def _datos_pdf(doc: DecaDocumento, envios: list, cambios: list) -> dict:
    return {
        "numero": doc.numero,
        "url": doc.url_descarga,
        "fecha_realizacion": _fmt_fecha(doc.fecha_realizacion),
        "fecha_creacion": _fmt_dt(doc.fecha_creacion),
        "fecha_modificacion": _fmt_dt(doc.fecha_modificacion),
        "fecha_creacion_dt": doc.fecha_creacion,
        "fecha_modificacion_dt": doc.fecha_modificacion,
        "contratante_nombre": doc.contratante_nombre,
        "contratante_nif": doc.contratante_nif,
        "contratante_domicilio": doc.contratante_domicilio,
        "transportista_nombre": doc.transportista_nombre,
        "transportista_nif": doc.transportista_nif,
        "transportista_domicilio": doc.transportista_domicilio,
        "conductor_nombre": doc.conductor_nombre,
        "conductor_nif": doc.conductor_nif,
        "conductor_telefono": doc.conductor_telefono,
        "matricula": doc.vehiculo_matricula,
        "remolque": doc.vehiculo_remolque,
        "vehiculo_descripcion": doc.vehiculo_descripcion,
        "autorizacion_especial": doc.autorizacion_especial,
        "observaciones": doc.observaciones,
        "envios": [
            {
                "orden": envio.orden,
                "origen": lugar_texto(envio.origen_lugar, envio.origen_direccion, envio.origen_cp, envio.origen_poblacion, envio.origen_provincia),
                "destino": lugar_texto(envio.destino_lugar, envio.destino_direccion, envio.destino_cp, envio.destino_poblacion, envio.destino_provincia),
                "naturaleza": envio.naturaleza,
                "peso": envio.peso,
            }
            for envio in envios
        ],
        "cambios": [
            {
                "fecha": _fmt_dt(cambio.fecha),
                "usuario": cambio.usuario or "",
                "motivo": cambio.motivo or "",
                "anterior": cambio.datos_anteriores or "",
            }
            for cambio in cambios
        ],
    }


def _exigir_nif(valor: str, etiqueta: str, obligatorio: bool) -> str:
    texto = normalizar_nif(valor)
    if not texto:
        if obligatorio:
            raise DecaError(f"El {etiqueta} necesita NIF.")
        return ""
    if not nif_valido(texto):
        raise DecaError(f"El NIF del {etiqueta} no es válido ({texto}).")
    return texto


def _guardar_parte(tipo: str, datos: dict, registro_id: int | None):
    spec = CATALOGOS[tipo]
    modelo = spec["model"]
    limpio = {}
    for nombre, etiqueta, obligatorio in spec["campos"]:
        if nombre == "nif":
            valor = normalizar_nif(datos.get(nombre, ""))
        elif nombre in ("matricula", "matricula_remolque"):
            valor = _mayus(datos.get(nombre, ""))
        else:
            valor = _limpiar(datos.get(nombre, ""))
        if obligatorio and len(valor) < 2:
            raise DecaError(f"Falta {etiqueta.lower()} en {spec['titulo'].lower()}.")
        limpio[nombre] = valor
    if tipo in ("transportista", "contratante"):
        limpio["nif"] = _exigir_nif(limpio.get("nif", ""), tipo, True)
    elif tipo == "conductor":
        limpio["nif"] = _exigir_nif(limpio.get("nif", ""), "conductor", False)
    if tipo == "contratante" and len(limpio.get("domicilio", "")) < 5:
        raise DecaError("El contratante del servicio necesita domicilio (nombre, NIF y domicilio son obligatorios).")
    if tipo == "vehiculo" and len(limpio.get("matricula", "")) < 4:
        raise DecaError("Indica la matrícula del vehículo.")

    fila = None
    if registro_id:
        fila = db.session.query(modelo).filter_by(id=registro_id).first()
    if fila is None and tipo in ("transportista", "contratante") and limpio.get("nif"):
        fila = db.session.query(modelo).filter_by(nif=limpio["nif"], activo=True).first()
    if fila is None and tipo == "conductor":
        if limpio.get("nif"):
            fila = db.session.query(modelo).filter_by(nif=limpio["nif"], activo=True).first()
        if fila is None and limpio.get("nombre"):
            fila = db.session.query(modelo).filter(
                DecaConductor.nombre == limpio["nombre"],
                DecaConductor.activo == True,
            ).first()
    if fila is None and tipo == "vehiculo" and limpio.get("matricula"):
        fila = db.session.query(modelo).filter_by(matricula=limpio["matricula"], activo=True).first()
    if fila is None and tipo in ("origen", "destino") and limpio.get("lugar"):
        fila = db.session.query(modelo).filter_by(
            tipo=spec["tipo_lugar"], lugar=limpio["lugar"], activo=True
        ).first()
    if fila is None:
        fila = modelo()
        db.session.add(fila)
    for clave, valor in limpio.items():
        setattr(fila, clave, valor)
    if tipo in ("origen", "destino"):
        fila.tipo = spec["tipo_lugar"]
    fila.activo = True
    db.session.flush()
    return fila


def _envios_crudos(form) -> list[dict]:
    claves = [
        "origen_id", "origen_lugar", "origen_direccion", "origen_cp", "origen_poblacion", "origen_provincia",
        "destino_id", "destino_lugar", "destino_direccion", "destino_cp", "destino_poblacion", "destino_provincia",
        "naturaleza", "peso",
    ]
    listas = {clave: form.getlist(clave) for clave in claves}
    total = max((len(valores) for valores in listas.values()), default=0)
    filas = []
    for i in range(total):
        fila = _envio_vacio()
        for clave in claves:
            valores = listas[clave]
            if i >= len(valores):
                continue
            if clave in ("origen_id", "destino_id"):
                fila[clave] = _id(valores[i])
            else:
                fila[clave] = _limpiar(valores[i])
        filas.append(fila)
    return filas or [_envio_vacio()]


def _envios_desde_form(form) -> list[dict]:
    claves = [
        "origen_id", "origen_lugar", "origen_direccion", "origen_cp", "origen_poblacion", "origen_provincia",
        "destino_id", "destino_lugar", "destino_direccion", "destino_cp", "destino_poblacion", "destino_provincia",
        "naturaleza", "peso",
    ]
    listas = {clave: form.getlist(clave) for clave in claves}
    total = len(listas["origen_lugar"])
    if not total or any(len(valores) != total for valores in listas.values()):
        raise DecaError("Los envíos del formulario están incompletos.")
    filas = []
    for i in range(total):
        fila = {clave: _limpiar(listas[clave][i]) for clave in claves}
        fila["origen_id"] = _id(listas["origen_id"][i])
        fila["destino_id"] = _id(listas["destino_id"][i])
        vacia = not any([
            fila["origen_lugar"], fila["destino_lugar"], fila["naturaleza"], fila["peso"],
            fila["origen_direccion"], fila["destino_direccion"],
        ])
        if vacia:
            continue
        if len(fila["origen_lugar"]) < 2 or len(fila["destino_lugar"]) < 2:
            raise DecaError(f"El envío {len(filas) + 1} necesita lugar de origen y lugar de destino.")
        if len(fila["naturaleza"]) < 2:
            raise DecaError(f"El envío {len(filas) + 1} necesita la naturaleza de la mercancía.")
        try:
            fila["peso"] = formato_peso(parse_peso(fila["peso"]))
        except ValueError:
            raise DecaError(f"El envío {len(filas) + 1} necesita un peso mayor que cero, en kilogramos.")
        filas.append(fila)
    if not filas:
        raise DecaError("Añade al menos un envío con origen, destino, naturaleza y peso.")
    return filas


def _datos_formulario(form, envios, mensajes=None):
    return {
        "id": (form.get("id") or "").strip(),
        "modo": (form.get("modo") or "nuevo").strip(),
        "fecha_realizacion": (form.get("fecha_realizacion") or "").strip(),
        "motivo": (form.get("motivo") or "").strip(),
        "transportista_id": (form.get("transportista_id") or "").strip(),
        "transportista_nombre": _limpiar(form.get("transportista_nombre")),
        "transportista_nif": _mayus(form.get("transportista_nif")),
        "transportista_domicilio": _limpiar(form.get("transportista_domicilio")),
        "transportista_telefono": _limpiar(form.get("transportista_telefono")),
        "contratante_id": (form.get("contratante_id") or "").strip(),
        "contratante_nombre": _limpiar(form.get("contratante_nombre")),
        "contratante_nif": _mayus(form.get("contratante_nif")),
        "contratante_domicilio": _limpiar(form.get("contratante_domicilio")),
        "contratante_telefono": _limpiar(form.get("contratante_telefono")),
        "conductor_id": (form.get("conductor_id") or "").strip(),
        "conductor_nombre": _limpiar(form.get("conductor_nombre")),
        "conductor_nif": _mayus(form.get("conductor_nif")),
        "conductor_telefono": _limpiar(form.get("conductor_telefono")),
        "vehiculo_id": (form.get("vehiculo_id") or "").strip(),
        "vehiculo_matricula": _mayus(form.get("vehiculo_matricula")),
        "vehiculo_remolque": _mayus(form.get("vehiculo_remolque")),
        "vehiculo_descripcion": _limpiar(form.get("vehiculo_descripcion")),
        "autorizacion_especial": _limpiar(form.get("autorizacion_especial")),
        "observaciones": (form.get("observaciones") or "").strip(),
        "envios": envios,
        "mensajes": mensajes or [],
        "numero": "",
        "url_descarga": "",
    }


def _datos_desde_documento(doc: DecaDocumento, envios: list, modo: str) -> dict:
    return {
        "id": "" if modo != "editar" else str(doc.id),
        "modo": modo,
        "fecha_realizacion": doc.fecha_realizacion.strftime("%Y-%m-%d") if doc.fecha_realizacion else "",
        "motivo": "",
        "transportista_id": str(doc.transportista_id or ""),
        "transportista_nombre": doc.transportista_nombre or "",
        "transportista_nif": doc.transportista_nif or "",
        "transportista_domicilio": doc.transportista_domicilio or "",
        "transportista_telefono": doc.transportista_telefono or "",
        "contratante_id": str(doc.contratante_id or ""),
        "contratante_nombre": doc.contratante_nombre or "",
        "contratante_nif": doc.contratante_nif or "",
        "contratante_domicilio": doc.contratante_domicilio or "",
        "contratante_telefono": doc.contratante_telefono or "",
        "conductor_id": str(doc.conductor_id or ""),
        "conductor_nombre": doc.conductor_nombre or "",
        "conductor_nif": doc.conductor_nif or "",
        "conductor_telefono": doc.conductor_telefono or "",
        "vehiculo_id": str(doc.vehiculo_id or ""),
        "vehiculo_matricula": doc.vehiculo_matricula or "",
        "vehiculo_remolque": doc.vehiculo_remolque or "",
        "vehiculo_descripcion": doc.vehiculo_descripcion or "",
        "autorizacion_especial": doc.autorizacion_especial or "",
        "observaciones": doc.observaciones or "",
        "envios": [
            {
                "origen_id": envio.origen_id,
                "origen_lugar": envio.origen_lugar,
                "origen_direccion": envio.origen_direccion,
                "origen_cp": envio.origen_cp,
                "origen_poblacion": envio.origen_poblacion,
                "origen_provincia": envio.origen_provincia,
                "destino_id": envio.destino_id,
                "destino_lugar": envio.destino_lugar,
                "destino_direccion": envio.destino_direccion,
                "destino_cp": envio.destino_cp,
                "destino_poblacion": envio.destino_poblacion,
                "destino_provincia": envio.destino_provincia,
                "naturaleza": envio.naturaleza,
                "peso": envio.peso,
            }
            for envio in envios
        ],
        "mensajes": [],
        "numero": doc.numero if modo == "editar" else "",
        "url_descarga": doc.url_descarga if modo == "editar" else "",
    }


def _vacio() -> dict:
    return {
        "id": "",
        "modo": "nuevo",
        "fecha_realizacion": date.today().strftime("%Y-%m-%d"),
        "motivo": "",
        "transportista_id": "",
        "transportista_nombre": "",
        "transportista_nif": "",
        "transportista_domicilio": "",
        "transportista_telefono": "",
        "contratante_id": "",
        "contratante_nombre": "",
        "contratante_nif": "",
        "contratante_domicilio": "",
        "contratante_telefono": "",
        "conductor_id": "",
        "conductor_nombre": "",
        "conductor_nif": "",
        "conductor_telefono": "",
        "vehiculo_id": "",
        "vehiculo_matricula": "",
        "vehiculo_remolque": "",
        "vehiculo_descripcion": "",
        "autorizacion_especial": "",
        "observaciones": "",
        "envios": [_envio_vacio()],
        "mensajes": [],
        "numero": "",
        "url_descarga": "",
    }


def _envio_vacio() -> dict:
    return {
        "origen_id": None,
        "origen_lugar": "",
        "origen_direccion": "",
        "origen_cp": "",
        "origen_poblacion": "",
        "origen_provincia": "",
        "destino_id": None,
        "destino_lugar": "",
        "destino_direccion": "",
        "destino_cp": "",
        "destino_poblacion": "",
        "destino_provincia": "",
        "naturaleza": "",
        "peso": "",
    }


def _listas_activas():
    return {
        "transportistas": db.session.query(DecaTransportista).filter_by(activo=True).order_by(DecaTransportista.nombre).all(),
        "contratantes": db.session.query(DecaContratante).filter_by(activo=True).order_by(DecaContratante.nombre).all(),
        "conductores": db.session.query(DecaConductor).filter_by(activo=True).order_by(DecaConductor.nombre).all(),
        "vehiculos": db.session.query(DecaVehiculoCat).filter_by(activo=True).order_by(DecaVehiculoCat.matricula).all(),
        "origenes": db.session.query(DecaLugar).filter_by(activo=True, tipo="origen").order_by(DecaLugar.lugar).all(),
        "destinos": db.session.query(DecaLugar).filter_by(activo=True, tipo="destino").order_by(DecaLugar.lugar).all(),
    }


def _render_form(datos):
    if not datos.get("envios"):
        datos["envios"] = [_envio_vacio()]
    return render_template("deca_form.html", datos=datos, listas=_listas_activas())


def _aplicar_documento(doc: DecaDocumento, form, envios_form: list[dict], momento: datetime) -> None:
    transportista = _guardar_parte("transportista", {
        "nombre": form.get("transportista_nombre"),
        "nif": form.get("transportista_nif"),
        "domicilio": form.get("transportista_domicilio"),
        "telefono": form.get("transportista_telefono"),
    }, _id(form.get("transportista_id")))
    contratante = _guardar_parte("contratante", {
        "nombre": form.get("contratante_nombre"),
        "nif": form.get("contratante_nif"),
        "domicilio": form.get("contratante_domicilio"),
        "telefono": form.get("contratante_telefono"),
    }, _id(form.get("contratante_id")))
    conductor = _guardar_parte("conductor", {
        "nombre": form.get("conductor_nombre"),
        "nif": form.get("conductor_nif"),
        "telefono": form.get("conductor_telefono"),
    }, _id(form.get("conductor_id")))
    vehiculo = _guardar_parte("vehiculo", {
        "matricula": form.get("vehiculo_matricula"),
        "matricula_remolque": form.get("vehiculo_remolque"),
        "descripcion": form.get("vehiculo_descripcion"),
    }, _id(form.get("vehiculo_id")))

    doc.transportista_id = transportista.id
    doc.transportista_nombre = transportista.nombre
    doc.transportista_nif = transportista.nif
    doc.transportista_domicilio = transportista.domicilio or ""
    doc.transportista_telefono = transportista.telefono or ""
    doc.contratante_id = contratante.id
    doc.contratante_nombre = contratante.nombre
    doc.contratante_nif = contratante.nif
    doc.contratante_domicilio = contratante.domicilio or ""
    doc.contratante_telefono = contratante.telefono or ""
    doc.conductor_id = conductor.id
    doc.conductor_nombre = conductor.nombre
    doc.conductor_nif = conductor.nif or ""
    doc.conductor_telefono = conductor.telefono or ""
    doc.vehiculo_id = vehiculo.id
    doc.vehiculo_matricula = vehiculo.matricula
    doc.vehiculo_remolque = vehiculo.matricula_remolque or ""
    doc.vehiculo_descripcion = vehiculo.descripcion or ""
    doc.autorizacion_especial = _limpiar(form.get("autorizacion_especial"))
    doc.observaciones = (form.get("observaciones") or "").strip()
    doc.fecha_modificacion = momento
    doc.usuario_modificacion = _usuario()

    if doc.id:
        db.session.query(DecaEnvio).filter_by(documento_id=doc.id).delete()
    else:
        db.session.flush()
    for indice, fila in enumerate(envios_form, start=1):
        origen = _guardar_parte("origen", {
            "lugar": fila["origen_lugar"],
            "direccion": fila["origen_direccion"],
            "cp": fila["origen_cp"],
            "poblacion": fila["origen_poblacion"],
            "provincia": fila["origen_provincia"],
        }, fila["origen_id"])
        destino = _guardar_parte("destino", {
            "lugar": fila["destino_lugar"],
            "direccion": fila["destino_direccion"],
            "cp": fila["destino_cp"],
            "poblacion": fila["destino_poblacion"],
            "provincia": fila["destino_provincia"],
        }, fila["destino_id"])
        db.session.add(DecaEnvio(
            documento_id=doc.id,
            orden=indice,
            origen_id=origen.id,
            origen_lugar=origen.lugar,
            origen_direccion=origen.direccion or "",
            origen_cp=origen.cp or "",
            origen_poblacion=origen.poblacion or "",
            origen_provincia=origen.provincia or "",
            destino_id=destino.id,
            destino_lugar=destino.lugar,
            destino_direccion=destino.direccion or "",
            destino_cp=destino.cp or "",
            destino_poblacion=destino.poblacion or "",
            destino_provincia=destino.provincia or "",
            naturaleza=fila["naturaleza"],
            peso=fila["peso"],
        ))


def _envios_de(doc_id: int) -> list:
    return db.session.query(DecaEnvio).filter_by(documento_id=doc_id).order_by(DecaEnvio.orden, DecaEnvio.id).all()


def _cambios_de(doc_id: int) -> list:
    return db.session.query(DecaCambio).filter_by(documento_id=doc_id).order_by(DecaCambio.fecha, DecaCambio.id).all()


def _generar_y_guardar(doc: DecaDocumento) -> None:
    envios = _envios_de(doc.id)
    cambios = _cambios_de(doc.id)
    contenido = generar_pdf_deca(_datos_pdf(doc, envios, cambios))
    _escribir_pdf(doc.token, contenido)


def _secciones_listas(error_tipo="", mensajes=None):
    secciones = []
    for tipo, spec in CATALOGOS.items():
        consulta = db.session.query(spec["model"]).filter_by(activo=True)
        if spec.get("tipo_lugar"):
            consulta = consulta.filter_by(tipo=spec["tipo_lugar"])
        filas = consulta.order_by(getattr(spec["model"], spec["orden"])).all()
        secciones.append({
            "tipo": tipo,
            "titulo": spec["titulo"],
            "ayuda": spec["ayuda"],
            "campos": spec["campos"],
            "filas": filas,
            "mensajes": mensajes if error_tipo == tipo else [],
        })
    return secciones


def _respuesta_pdf(doc: DecaDocumento):
    ruta = _ruta_pdf(doc.token)
    if not os.path.isfile(ruta):
        _generar_y_guardar(doc)
        db.session.commit()
    return send_file(
        ruta,
        mimetype="application/pdf",
        as_attachment=False,
        download_name=f"{doc.numero.replace('/', '-')}.pdf",
        max_age=0,
        conditional=False,
    )


def register_deca_routes(app):

    @app.route("/deca")
    @login_required
    def deca_lista():
        documentos = db.session.query(DecaDocumento).filter_by(activo=True).order_by(DecaDocumento.id.desc()).all()
        ids = [doc.id for doc in documentos]
        envios = []
        if ids:
            envios = db.session.query(DecaEnvio).filter(DecaEnvio.documento_id.in_(ids)).order_by(DecaEnvio.orden).all()
        por_doc = {}
        for envio in envios:
            por_doc.setdefault(envio.documento_id, []).append(envio)
        filas = []
        for doc in documentos:
            viajes = por_doc.get(doc.id, [])
            if viajes:
                primero = viajes[0]
                ruta = (
                    f"{primero.origen_lugar} → {primero.destino_lugar}"
                    + (f" (+{len(viajes) - 1})" if len(viajes) > 1 else "")
                )
                mercancia = primero.naturaleza
            else:
                ruta = ""
                mercancia = ""
            filas.append({
                "doc": doc,
                "ruta": ruta,
                "mercancia": mercancia,
                "fecha": _fmt_fecha(doc.fecha_realizacion),
                "https": (doc.url_descarga or "").lower().startswith("https://"),
            })
        aviso_https = any(not fila["https"] for fila in filas)
        return render_template("deca_lista.html", filas=filas, aviso_https=aviso_https)

    @app.route("/deca/nuevo")
    @login_required
    def deca_nuevo():
        desde = request.args.get("desde", type=int)
        if not desde:
            return _render_form(_vacio())
        doc = db.session.query(DecaDocumento).filter_by(id=desde, activo=True).first()
        if not doc:
            return redirect(url_for("deca_nuevo"))
        datos = _datos_desde_documento(doc, _envios_de(doc.id), "reutilizar")
        datos["fecha_realizacion"] = date.today().strftime("%Y-%m-%d")
        datos["mensajes"] = [f"Datos copiados de {doc.numero}. Al guardar se crea un DeCA nuevo, con otra URL y otro QR."]
        return _render_form(datos)

    @app.route("/deca/documento/<int:doc_id>/editar")
    @login_required
    def deca_editar(doc_id):
        doc = db.session.query(DecaDocumento).filter_by(id=doc_id, activo=True).first()
        if not doc:
            return redirect(url_for("deca_lista"))
        return _render_form(_datos_desde_documento(doc, _envios_de(doc.id), "editar"))

    @app.route("/deca/guardar", methods=["POST"])
    @login_required
    def deca_guardar():
        form = request.form
        try:
            envios_form = _envios_desde_form(form)
        except DecaError as exc:
            return _render_form(_datos_formulario(form, _envios_crudos(form), exc.mensajes))
        doc_id = _id(form.get("id"))
        modo = (form.get("modo") or "").strip()
        try:
            fecha_txt = (form.get("fecha_realizacion") or "").strip()
            try:
                fecha = datetime.strptime(fecha_txt, "%Y-%m-%d").date()
            except ValueError:
                raise DecaError("Indica la fecha de realización del transporte.")
            if len(_limpiar(form.get("conductor_nombre"))) < 2:
                raise DecaError("Indica el conductor.")
            ahora = datetime.now().replace(microsecond=0)
            if doc_id and modo == "editar":
                doc = db.session.query(DecaDocumento).filter_by(id=doc_id, activo=True).first()
                if not doc:
                    raise DecaError("El DeCA que quieres modificar ya no está disponible.")
                motivo = (form.get("motivo") or "").strip()
                if len(motivo) < 3:
                    raise DecaError("Para modificar un DeCA ya emitido hay que indicar el motivo. Se conserva el dato anterior y el mismo QR.")
                anteriores = _envios_de(doc.id)
                db.session.add(DecaCambio(
                    documento_id=doc.id,
                    fecha=ahora,
                    usuario=_usuario(),
                    motivo=motivo,
                    datos_anteriores=_resumen(doc, anteriores),
                ))
            else:
                token = secrets.token_urlsafe(18)
                doc = DecaDocumento(
                    numero=_siguiente_numero(ahora),
                    token=token,
                    url_descarga=_url_publica(token),
                    fecha_realizacion=fecha,
                    fecha_creacion=ahora,
                    fecha_modificacion=ahora,
                    usuario_creacion=_usuario(),
                    usuario_modificacion=_usuario(),
                    activo=True,
                )
                db.session.add(doc)
                db.session.flush()
            doc.fecha_realizacion = fecha
            _aplicar_documento(doc, form, envios_form, ahora)
            db.session.flush()
            _generar_y_guardar(doc)
            db.session.commit()
            return redirect(url_for("deca_lista"))
        except DecaError as exc:
            db.session.rollback()
            datos = _datos_formulario(form, envios_form, exc.mensajes)
            if doc_id and modo == "editar":
                previo = db.session.query(DecaDocumento).filter_by(id=doc_id).first()
                if previo:
                    datos["numero"] = previo.numero
                    datos["url_descarga"] = previo.url_descarga
            return _render_form(datos)
        except Exception as exc:
            db.session.rollback()
            datos = _datos_formulario(form, envios_form, [f"No se ha podido generar el DeCA: {exc}"])
            return _render_form(datos)

    @app.route("/deca/documento/<int:doc_id>/pdf")
    @login_required
    def deca_pdf(doc_id):
        doc = db.session.query(DecaDocumento).filter_by(id=doc_id, activo=True).first()
        if not doc:
            return redirect(url_for("deca_lista"))
        respuesta = _respuesta_pdf(doc)
        respuesta.headers["Cache-Control"] = "no-store"
        return respuesta

    @app.route("/deca/d/<token>")
    def deca_descarga_publica(token):
        """Descarga directa del PDF. Sin login, sin página intermedia y sin botón."""
        if not _TOKEN_RE.match(token or ""):
            return ("Documento no encontrado", 404)
        doc = db.session.query(DecaDocumento).filter_by(token=token, activo=True).first()
        if not doc:
            return ("Documento no encontrado", 404)
        respuesta = _respuesta_pdf(doc)
        respuesta.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
        respuesta.headers["Pragma"] = "no-cache"
        respuesta.headers["X-Content-Type-Options"] = "nosniff"
        return respuesta

    @app.route("/deca/listas", methods=["GET"])
    @login_required
    def deca_listas():
        return render_template("deca_listas.html", secciones=_secciones_listas(), mensajes=[])

    @app.route("/deca/listas/guardar", methods=["POST"])
    @login_required
    def deca_guardar_lista():
        tipo = (request.form.get("tipo") or "").strip()
        if tipo not in CATALOGOS:
            return redirect(url_for("deca_listas"))
        spec = CATALOGOS[tipo]
        datos = {nombre: request.form.get(nombre, "") for nombre, _etiq, _req in spec["campos"]}
        try:
            _guardar_parte(tipo, datos, _id(request.form.get("id")))
            db.session.commit()
            return redirect(url_for("deca_listas") + f"#{tipo}")
        except DecaError as exc:
            db.session.rollback()
            return render_template(
                "deca_listas.html",
                secciones=_secciones_listas(tipo, exc.mensajes),
                mensajes=exc.mensajes,
            )

    @app.route("/deca/listas/archivar", methods=["POST"])
    @login_required
    def deca_archivar_lista():
        tipo = (request.form.get("tipo") or "").strip()
        registro_id = _id(request.form.get("id"))
        if tipo in CATALOGOS and registro_id:
            fila = db.session.query(CATALOGOS[tipo]["model"]).filter_by(id=registro_id).first()
            if fila:
                fila.activo = False
                db.session.commit()
        return redirect(url_for("deca_listas") + f"#{tipo if tipo in CATALOGOS else ''}")
