"""PDF nativo del documento electrónico de control administrativo (DeCA)."""
from __future__ import annotations

from datetime import datetime

import fitz

NAVY = (14 / 255, 42 / 255, 74 / 255)
INK = (0.10, 0.12, 0.16)
MUTED = (0.33, 0.36, 0.40)
LINE = (0.75, 0.78, 0.82)
PAPER = (0.945, 0.953, 0.962)
WHITE = (1, 1, 1)
MAX_BYTES = 5 * 1024 * 1024

ANCHO = 595.276
ALTO = 841.890
MARGEN = 32


def generar_pdf_deca(datos: dict) -> bytes:
    """Genera el PDF en memoria. El QR contiene la URL de descarga directa."""
    doc = fitz.open()
    qr = _CodigoQR(datos["url"])
    lienzo = _Lienzo(doc, datos, qr)
    lienzo.dibujar()
    meta_creacion = _pdf_fecha(datos["fecha_creacion_dt"])
    meta_mod = _pdf_fecha(datos["fecha_modificacion_dt"])
    doc.set_metadata({
        "title": f"DeCA {datos['numero']}",
        "author": datos.get("transportista_nombre") or "Transportista efectivo",
        "subject": "Documento electronico de control administrativo (DeCA)",
        "keywords": "DeCA, Orden FOM/2861/2012, control administrativo",
        "creator": "Alditraex DeCA",
        "producer": "Alditraex DeCA",
        "creationDate": meta_creacion,
        "modDate": meta_mod,
    })
    contenido = doc.tobytes(garbage=4, deflate=True)
    doc.close()
    if not contenido.startswith(b"%PDF"):
        raise ValueError("El fichero generado no es un PDF nativo.")
    if len(contenido) > MAX_BYTES:
        raise ValueError("El PDF supera el maximo de 5 MB de la resolucion DeCA.")
    return contenido


def _pdf_fecha(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.now().astimezone().tzinfo)
    zona = dt.strftime("%z") or "+0000"
    zona = zona[:3] + "'" + zona[3:] + "'"
    return dt.strftime("D:%Y%m%d%H%M%S") + zona


def _sanear(texto) -> str:
    if texto is None:
        return ""
    return str(texto).replace("\u2014", "-").replace("\u2013", "-").encode("latin-1", "replace").decode("latin-1")


def _ancho(texto: str, fontsize: float, fontname: str = "helv") -> float:
    try:
        return fitz.get_text_length(texto, fontname=fontname, fontsize=fontsize)
    except Exception:
        return len(texto) * fontsize * 0.52


def _partir(texto: str, fontsize: float, ancho: float, fontname: str = "helv") -> list[str]:
    texto = _sanear(texto).replace("\r", "")
    if not texto.strip():
        return [""]
    lineas = []
    for parrafo in texto.split("\n"):
        palabras = parrafo.split()
        if not palabras:
            lineas.append("")
            continue
        actual = ""
        for palabra in palabras:
            prueba = palabra if not actual else actual + " " + palabra
            if _ancho(prueba, fontsize, fontname) <= ancho:
                actual = prueba
                continue
            if actual:
                lineas.append(actual)
            if _ancho(palabra, fontsize, fontname) <= ancho:
                actual = palabra
                continue
            trozo = ""
            for caracter in palabra:
                if _ancho(trozo + caracter, fontsize, fontname) <= ancho:
                    trozo += caracter
                else:
                    if trozo:
                        lineas.append(trozo)
                    trozo = caracter
            actual = trozo
        if actual:
            lineas.append(actual)
    return lineas or [""]


class _CodigoQR:
    def __init__(self, url: str):
        import segno

        qr = segno.make(url, error="m")
        self.url = url
        self.matrix = [list(fila) for fila in qr.matrix]
        self.n = len(self.matrix) or 1

    def dibujar(self, page, x: float, y: float, size: float) -> None:
        page.draw_rect(
            fitz.Rect(x - 3, y - 3, x + size + 3, y + size + 3),
            color=WHITE,
            fill=WHITE,
            width=0,
        )
        celda = size / self.n
        for fila_i, fila in enumerate(self.matrix):
            for col_i, modulo in enumerate(fila):
                if not modulo:
                    continue
                page.draw_rect(
                    fitz.Rect(
                        x + col_i * celda,
                        y + fila_i * celda,
                        x + (col_i + 1) * celda + 0.15,
                        y + (fila_i + 1) * celda + 0.15,
                    ),
                    color=(0, 0, 0),
                    fill=(0, 0, 0),
                    width=0,
                )
        page.insert_link({
            "kind": fitz.LINK_URI,
            "from": fitz.Rect(x - 3, y - 3, x + size + 3, y + size + 3),
            "uri": self.url,
        })


class _Lienzo:
    def __init__(self, doc, datos: dict, qr: _CodigoQR):
        self.doc = doc
        self.datos = datos
        self.qr = qr
        self.page = None
        self.y = 0
        self.primera = True
        self.limite = 792

    def dibujar(self) -> None:
        self._nueva_pagina()
        d = self.datos
        self._linea_meta(
            f"N.º {d['numero']}",
            f"Fecha del transporte: {d['fecha_realizacion']}",
        )
        self._linea_meta(
            f"Creación: {d['fecha_creacion']}",
            f"Última modificación: {d['fecha_modificacion']}",
        )
        self._nota(
            "Transporte público de mercancías por carretera. Orden FOM/2861/2012 y resolución DeCA.\n"
            "Documento administrativo: no sustituye a la carta de porte ni al CMR."
        )
        self._seccion("A. Cargador contractual (contratante del servicio)")
        self._ficha([
            ("Nombre o denominación social", d["contratante_nombre"]),
            ("NIF", d["contratante_nif"]),
            ("Domicilio", d["contratante_domicilio"]),
        ])
        self._seccion("B. Transportista efectivo")
        self._ficha([
            ("Nombre o denominación social", d["transportista_nombre"]),
            ("NIF", d["transportista_nif"]),
            ("Domicilio", d["transportista_domicilio"] or "No consta"),
        ])
        self._seccion("C y D. Envíos: origen, destino, naturaleza y peso")
        self._nota(f"F. Fecha de realización del transporte: {d['fecha_realizacion']}")
        if len(d["envios"]) > 1:
            self._nota(
                "Varios envíos agrupados en este DeCA. Mismo cargador contractual y mismo transportista efectivo. "
                "Cada envío queda identificado por origen, destino y mercancía."
            )
        self._tabla_envios(d["envios"])
        self._seccion("E. Autorización especial de circulación")
        self._parrafo(d["autorizacion_especial"] or "No consta. No aplica autorización especial de circulación.")
        self._seccion("G. Matrícula del vehículo")
        vehiculo = f"Vehículo motor: {d['matricula']}"
        if d.get("remolque"):
            vehiculo += f"    Remolque o semirremolque: {d['remolque']}"
        if d.get("vehiculo_descripcion"):
            vehiculo += f"\n{d['vehiculo_descripcion']}"
        self._parrafo(vehiculo)
        self._seccion("H. Observaciones")
        self._parrafo(d["observaciones"] or "Sin observaciones.")
        self._seccion("Conductor del vehículo")
        conductor = d["conductor_nombre"]
        if d.get("conductor_nif"):
            conductor += f"  |  NIF/DNI: {d['conductor_nif']}"
        if d.get("conductor_telefono"):
            conductor += f"  |  Tel.: {d['conductor_telefono']}"
        self._parrafo(conductor)
        self._seccion("Modificaciones durante el servicio")
        if not d["cambios"]:
            self._parrafo("Sin modificaciones posteriores a la emisión. Misma URL y mismo QR desde el alta.")
        else:
            self._nota(
                "Cada cambio conserva los datos anteriores y el motivo. La URL y el QR no cambian."
            )
            for cambio in d["cambios"]:
                self._parrafo(
                    f"{cambio['fecha']}  |  {cambio['usuario']}\n"
                    f"Motivo: {cambio['motivo']}\n"
                    f"Datos anteriores:\n{cambio['anterior']}",
                    fontsize=8,
                )
                self.y += 4
        self._seccion("Copia para el conductor y control en carretera")
        self._parrafo(
            "La copia puede ser digital o impresa y debe incluir este QR. "
            "Las anotaciones manuscritas no se tienen en cuenta.\n"
            "La URL abre el PDF directamente, sin usuario, contraseña ni botón de descarga.\n"
            f"URL: {d['url']}\n"
            "Conservación del fichero: mínimo un año. "
            "El documento debe existir antes del inicio efectivo del servicio."
        )
        total = self.doc.page_count
        for indice, pagina in enumerate(self.doc):
            pagina.insert_text(
                (MARGEN, 828),
                _sanear(f"Página {indice + 1} de {total}   |   {d['numero']}   |   PDF nativo digital"),
                fontsize=8,
                fontname="helv",
                color=MUTED,
            )

    def _nueva_pagina(self) -> None:
        self.page = self.doc.new_page(width=ANCHO, height=ALTO)
        self._cabecera()
        self.primera = False

    def _cabecera(self) -> None:
        alto_barra = 78 if self.primera else 62
        self.page.draw_rect(fitz.Rect(0, 0, ANCHO, alto_barra), color=NAVY, fill=NAVY, width=0)
        qr_size = 58 if self.primera else 46
        qr_x = ANCHO - MARGEN - qr_size
        qr_y = 8
        self.qr.dibujar(self.page, qr_x, qr_y, qr_size)
        self.page.insert_text(
            (MARGEN, 22),
            "DOCUMENTO ELECTRÓNICO DE CONTROL ADMINISTRATIVO",
            fontsize=8.5,
            fontname="hebo",
            color=WHITE,
        )
        self.page.insert_text((MARGEN, 40), "DeCA", fontsize=16, fontname="hebo", color=WHITE)
        subtitulo = "Mercancías por carretera" if self.primera else _sanear(f"Continuación  |  {self.datos['numero']}")
        self.page.insert_text((MARGEN, 56), subtitulo, fontsize=9, fontname="helv", color=(0.82, 0.86, 0.90))
        if self.primera:
            self.page.insert_text(
                (MARGEN, 70),
                "Acceso directo mediante el código QR",
                fontsize=8,
                fontname="helv",
                color=(0.82, 0.86, 0.90),
            )
        self.y = alto_barra + 16

    def _hueco(self, alto: float) -> bool:
        if self.y + alto <= self.limite:
            return False
        self._nueva_pagina()
        return True

    def _linea_meta(self, izquierda: str, derecha: str) -> None:
        self._hueco(14)
        self.page.insert_text((MARGEN, self.y + 10), _sanear(izquierda), fontsize=9, fontname="hebo", color=INK)
        self.page.insert_text((300, self.y + 10), _sanear(derecha), fontsize=9, fontname="helv", color=INK)
        self.y += 14

    def _nota(self, texto: str) -> None:
        self._parrafo(texto, fontsize=8, color=MUTED)

    def _seccion(self, titulo: str) -> None:
        self._hueco(22)
        self.y += 6
        rect = fitz.Rect(MARGEN, self.y, ANCHO - MARGEN, self.y + 15)
        self.page.draw_rect(rect, color=NAVY, fill=NAVY, width=0)
        self.page.insert_text((MARGEN + 6, self.y + 11), _sanear(titulo), fontsize=9, fontname="hebo", color=WHITE)
        self.y += 20

    def _ficha(self, pares: list[tuple[str, str]]) -> None:
        for etiqueta, valor in pares:
            self._parrafo(f"{etiqueta}: {valor or '-'}", fontsize=9)

    def _parrafo(self, texto: str, fontsize: float = 9, color=INK) -> None:
        ancho = ANCHO - (MARGEN * 2)
        for linea in _partir(texto, fontsize, ancho):
            self._hueco(fontsize + 4)
            self.page.insert_text(
                (MARGEN, self.y + fontsize),
                linea if linea else " ",
                fontsize=fontsize,
                fontname="helv",
                color=color,
            )
            self.y += fontsize + 3

    def _tabla_envios(self, envios: list[dict]) -> None:
        anchos = [28, 145, 145, 130, 83]
        cabeceras = ["N.º", "Origen", "Destino", "Naturaleza", "Peso"]
        self._fila_tabla(cabeceras, anchos, cabecera=True)
        for envio in envios:
            self._fila_tabla(
                [
                    str(envio["orden"]),
                    envio["origen"],
                    envio["destino"],
                    envio["naturaleza"],
                    f"{envio['peso']} kg",
                ],
                anchos,
                cabecera=False,
            )

    def _fila_tabla(self, celdas: list[str], anchos: list[int], cabecera: bool) -> None:
        fontsize = 8
        columnas = []
        alto = 16
        for texto, ancho in zip(celdas, anchos):
            lineas = _partir(texto, fontsize, ancho - 8)
            columnas.append(lineas)
            alto = max(alto, 8 + len(lineas) * (fontsize + 2))
        salto = self._hueco(alto + 2)
        if salto and not cabecera:
            self._fila_tabla(["N.º", "Origen", "Destino", "Naturaleza", "Peso"], anchos, cabecera=True)
            self._hueco(alto + 2)
        x = MARGEN
        y0 = self.y
        relleno = NAVY if cabecera else PAPER
        tinta = WHITE if cabecera else INK
        fuente = "hebo" if cabecera else "helv"
        for lineas, ancho in zip(columnas, anchos):
            rect = fitz.Rect(x, y0, x + ancho, y0 + alto)
            self.page.draw_rect(rect, color=LINE, fill=relleno, width=0.4)
            yy = y0 + 11
            for linea in lineas:
                self.page.insert_text((x + 4, yy), linea, fontsize=fontsize, fontname=fuente, color=tinta)
                yy += fontsize + 2
            x += ancho
        self.y += alto
