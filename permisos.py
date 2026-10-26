"""Permisos de acceso por usuario a módulos de la aplicación.

La lista PERMISOS_USUARIO es la asignación inicial. Al arrancar se copia a la
columna usuario.permisos y, a partir de ahí, manda lo guardado desde el manager.
"""
from __future__ import annotations

import json

from flask import g, has_request_context
from sqlalchemy import func

import db
from models import Usuario

# Orden de las casillas del manager. Calidad no entra en el acceso completo:
# quien tiene el resto marcado sigue sin Calidad hasta que se marque.
MODULOS = (
    ("dashboard", "Vehículos"),
    ("aldipod", "Aldipod"),
    ("caja", "Contados"),
    ("caja_reembolsos", "Reembolsos"),
    ("presupuestos", "Presupuestos"),
    ("ordenes_carga", "Órdenes"),
    ("deca", "DeCa"),
    ("llegadas", "Llegadas"),
    ("rectificaciones", "Rectificaciones"),
    ("vacaciones", "Vacaciones"),
    ("email", "Email"),
    ("ftp", "FTP"),
    ("ficheros", "Ficheros"),
    ("manager", "Manager"),
    ("calidad", "Calidad"),
)

USUARIO_FIJO = "jmurillo"
CALIDAD_INICIAL = frozenset({"jmurillo", "pserrano", "rrodriguez"})
GESTORES_MANAGER = frozenset({"pserrano", "rrodriguez"})

TODOS_MODULOS = frozenset(mid for mid, _etiqueta in MODULOS)
MODULOS_GENERAL = frozenset(mid for mid in TODOS_MODULOS if mid != "calidad")
ALL_MODULOS = MODULOS_GENERAL

# '*' = acceso total
PERMISOS_USUARIO = {
    "jmurillo": frozenset({"*"}),
    "rocio": frozenset({"*"}),
    "pserrano": frozenset({"*"}),
    "javimurillo": frozenset({"*"}),
    "jamurillo": frozenset({"*"}),  # alias histórico
    "padiaz": frozenset({"rectificaciones", "aldipod","deca"}),
    "fbonilla": frozenset({"rectificaciones", "aldipod", "caja", "deca", "presupuestos"}),
    "aespino": frozenset({"rectificaciones", "aldipod", "deca", "llegadas", "presupuestos"}),
    "amoreno": frozenset({"rectificaciones", "aldipod","llegadas", "presupuestos", "deca"}),
    "mjbejarano": frozenset({"presupuestos", "rectificaciones"}),
    "amesonero": frozenset({"presupuestos","deca", "rectificaciones"}),
    "pcortes": frozenset({"caja","deca", "rectificaciones"}),
    "vbejarano": frozenset({"deca", "rectificaciones","llegadas"}),
    "ctrinidad": frozenset({"rectificaciones", "aldipod","llegadas", "caja", "deca"}),
    "icastro": frozenset({
        "presupuestos",
        "ordenes_carga",
        "deca",
        "llegadas",
        "vacaciones",
        "rectificaciones",
    }),
    "djimenez": frozenset({
        "presupuestos",
        "ordenes_carga",
        "deca",
        "llegadas",
        "vacaciones",
        "rectificaciones",
    }),
    "jadiaz": frozenset({
        "presupuestos",
        "ordenes_carga",
        "deca",
        "llegadas",
        "vacaciones",
        "rectificaciones",
    }),
    "mgallego": frozenset({"llegadas", "caja_reembolsos", "aldipod", "deca"}),
    "bgarcia": frozenset({"rectificaciones", "aldipod","llegadas", "caja", "deca"}),
}

# Prefijos de ruta por módulo (orden: más específicos primero en la comprobación)
# /caja no debe confundirse con /caja-reembolsos
RUTAS_POR_MODULO = {
    "aldipod": (
        "/registro_incidencias_aldipod",
        "/incidencia_aldipod/",
        "/aldipod/",
        "/descargar_imagen/",
    ),
    "caja_reembolsos": ("/caja-reembolsos",),
    "caja": ("/caja",),  # Contados; se excluye caja-reembolsos en el matcher
    "presupuestos": (
        "/presupuestos",
        "/presupuestos_todos",
        "/formulario_presupuesto",
        "/siguiente_numero_presupuesto",
        "/crear_cliente_presupuesto",
        "/borrar_presupuesto/",
        "/crear_presupuesto",
        "/exportar_presupuesto_pdf/",
        "/exportar_presupuestos_excel",
        "/form_editar_presupuesto/",
        "/modificar_presupuesto",
        "/generar_factura_proforma/",
        "/exportar_factura_proforma_pdf/",
    ),
    "ordenes_carga": (
        "/ordenes_carga_internacionales",
        "/api/ordenes_carga/",
    ),
    "deca": (
        "/deca",
    ),
    "llegadas": (
        "/llegadas-camiones",
        "/api/llegadas-camiones",
    ),
    "rectificaciones": (
        "/rectificaciones",
        "/api/rectificaciones",
    ),
    "vacaciones": (
        "/vacaciones",
        "/api/vacaciones",
    ),
    "dashboard": (
        "/index",
        "/vehiculos",
        "/itv",
        "/seguros",
        "/tacografos",
        "/rodajes",
        "/extintores",
        "/talleres",
        "/transpaletas",
        "/ficha",
        "/tareas",
        "/gasoil",
        "/crear_",
        "/form_editar_",
        "/tickets",
        "/selector",
    ),
    "manager": (
        "/manager",
        "/crear_usuario",
        "/borrar_usuario",
        "/formulario_usuario",
        "/guardar_permisos",
        "/editar_usuario",
        "/form_editar_usuario",
    ),
    "email": ("/email_destinatarios",),
    "ftp": ("/ftp_transfer",),
    "ficheros": ("/ficheros",),
    "calidad": ("/calidad",),
}

RUTAS_SIEMPRE = frozenset({
    "/",
    "/portada",
    "/login",
    "/logout",
})


def _norm(username: str | None) -> str:
    return (username or "").strip().lower()


def _json_inicial(username: str) -> str | None:
    """Valor para la columna cuando todavía está vacía. None = dejar el acceso anterior."""
    if username == USUARIO_FIJO:
        return "*"
    base = PERMISOS_USUARIO.get(username)
    if base is None:
        return None
    if "*" in base:
        mods = set(MODULOS_GENERAL)
        if username in CALIDAD_INICIAL:
            mods.add("calidad")
        return json.dumps(sorted(mods))
    return json.dumps(sorted(m for m in base if m in TODOS_MODULOS))


def _mods_uncached(username: str) -> frozenset[str] | None:
    """None = usuario sin ficha de permisos: conserva el acceso que tenía."""
    if username == USUARIO_FIJO:
        return TODOS_MODULOS
    fila = db.session.query(Usuario).filter(func.lower(Usuario.username) == username).first()
    raw = (fila.permisos if fila is not None else None) or ""
    raw = raw.strip()
    if not raw:
        inicial = _json_inicial(username)
        if inicial is None:
            return None
        raw = inicial
    if raw == "*":
        return TODOS_MODULOS
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return TODOS_MODULOS
    if not isinstance(data, list):
        return TODOS_MODULOS
    mods = frozenset(str(x) for x in data if str(x) in TODOS_MODULOS)
    if username in GESTORES_MANAGER:
        mods = mods | {"manager"}
    return mods


def _mods(username: str | None) -> frozenset[str] | None:
    u = _norm(username)
    if not has_request_context():
        return _mods_uncached(u)
    cache = getattr(g, "_mods_cache", None)
    if cache is None:
        cache = {}
        g._mods_cache = cache
    if u not in cache:
        cache[u] = _mods_uncached(u)
    return cache[u]


def acceso_total(username: str | None) -> bool:
    mods = _mods(username)
    if mods is None:
        return False
    return MODULOS_GENERAL <= mods


def tiene_restriccion(username: str | None) -> bool:
    """True si el usuario tiene una ficha de accesos y no es acceso completo."""
    mods = _mods(username)
    if mods is None:
        return False
    return not (MODULOS_GENERAL <= mods)


def permisos_guardados(username: str | None) -> bool:
    """True si el manager ya guardó una ficha para este usuario."""
    u = _norm(username)
    if u == USUARIO_FIJO:
        return True
    fila = db.session.query(Usuario).filter(func.lower(Usuario.username) == u).first()
    return bool(fila is not None and (fila.permisos or "").strip())


def permisos_usuario(username: str | None) -> frozenset[str] | None:
    """
    Módulos que hay que pintar.
    None = sin ficha: la portada sigue con el comportamiento anterior.
    """
    return _mods(username)


def puede(username: str | None, modulo: str) -> bool:
    if _norm(username) == USUARIO_FIJO:
        return True
    mods = _mods(username)
    if mods is None:
        if modulo == "calidad":
            return _norm(username) in CALIDAD_INICIAL
        return True
    if modulo == "calidad":
        return "calidad" in mods
    if MODULOS_GENERAL <= mods:
        return True
    return modulo in mods


def marcas_para_formulario(username: str | None) -> tuple[frozenset[str], str]:
    """Casillas marcadas y si la ficha es fija, heredada o ya guardada."""
    u = _norm(username)
    if u == USUARIO_FIJO:
        return TODOS_MODULOS, "fijo"
    mods = _mods(u)
    if mods is None:
        marcas = set(MODULOS_GENERAL)
        if u in CALIDAD_INICIAL:
            marcas.add("calidad")
        return frozenset(marcas), "legacy"
    return mods, "acl"


def guardar_permisos_de_usuarios(seleccion: dict[int, set[str]]) -> None:
    """Guarda las casillas. jmurillo no se toca. Quien no cambia y no tenía ficha, sigue igual."""
    if not seleccion:
        return
    ids = list(seleccion)
    filas = db.session.query(Usuario).filter(Usuario.id.in_(ids)).all()
    for fila in filas:
        nombre = _norm(fila.username)
        if nombre == USUARIO_FIJO:
            fila.permisos = "*"
            continue
        posted = {m for m in seleccion.get(fila.id, set()) if m in TODOS_MODULOS}
        if nombre in GESTORES_MANAGER:
            posted.add("manager")
        marcas, tipo = marcas_para_formulario(nombre)
        if tipo == "legacy" and posted == set(marcas):
            continue
        if MODULOS_GENERAL <= posted and "calidad" in posted:
            fila.permisos = "*"
        else:
            fila.permisos = json.dumps(sorted(posted))
    db.session.commit()
    if has_request_context():
        g.pop("_mods_cache", None)


def sembrar_permisos() -> None:
    """Copia la asignación inicial a los usuarios que aún no tienen ficha."""
    ses = db.get_session()
    try:
        for fila in ses.query(Usuario).all():
            nombre = _norm(fila.username)
            actual = (fila.permisos or "").strip()
            if nombre == USUARIO_FIJO:
                if actual != "*":
                    fila.permisos = "*"
                continue
            if actual == "*":
                continue
            if actual:
                if nombre in GESTORES_MANAGER:
                    try:
                        data = json.loads(actual)
                    except json.JSONDecodeError:
                        data = None
                    if isinstance(data, list) and "manager" not in data:
                        data.append("manager")
                        fila.permisos = json.dumps(sorted(set(data)))
                continue
            inicial = _json_inicial(nombre)
            if inicial is not None:
                fila.permisos = inicial
        ses.commit()
    finally:
        ses.close()


def _path_cubre(path: str, prefix: str) -> bool:
    if path == prefix:
        return True
    if prefix.endswith("/"):
        return path.startswith(prefix)
    return path.startswith(prefix + "/")


def ruta_permitida(username: str | None, path: str) -> bool:
    """Comprueba si un path está permitido para el usuario (si tiene ACL limitada)."""
    path = path or "/"
    if path == "/calidad" or path.startswith("/calidad/"):
        return puede(username, "calidad")
    if acceso_total(username):
        return True
    if not tiene_restriccion(username):
        return True

    p = permisos_usuario(username) or frozenset()
    path = path or "/"
    if path in RUTAS_SIEMPRE or path.startswith("/static/"):
        return True
    # Documentación pública: cualquier usuario autenticado, tenga o no ACL.
    if path == "/documentacion-publica" or path.startswith("/documentacion-publica/"):
        return True
    # Tarifa Alditraex y KPIs: mismo acceso que la documentación pública.
    if path == "/tarifa-alditraex" or path.startswith("/tarifa-alditraex/"):
        return True
    if path == "/kpis" or path.startswith("/kpis/"):
        return True
    # Horario semanal: todos pueden verlo. Subir y quitar se controla en la vista.
    if path == "/horario-semanal" or path.startswith("/horario-semanal/"):
        return True
    # El QR del DeCA tiene que abrir el PDF sin login y sin más pasos.
    if path.startswith("/deca/d/"):
        return True

    # Descarga de BD: solo acceso total (ya cubierto arriba); restringidos no
    if path == "/descargar_db":
        return False

    # Contados: /caja pero no /caja-reembolsos
    for modulo in p:
        prefixes = RUTAS_POR_MODULO.get(modulo, ())
        for pref in prefixes:
            if modulo == "caja":
                if path == "/caja" or path.startswith("/caja/"):
                    return True
                continue
            if _path_cubre(path, pref):
                return True
    return False
