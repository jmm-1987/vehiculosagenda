"""Convierte HTML de impresión a PDF y fusiona adjuntos con PyMuPDF."""
from __future__ import annotations

import io
import os

import fitz


def _css_pdf(archive: str | None) -> str:
    if not archive:
        return ""
    path = os.path.join(archive, "orden_carga_pdf.css")
    if not os.path.isfile(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


def html_a_pdf_bytes(html: str, archive: str | None = None) -> bytes:
    """Renderiza HTML a PDF A4 usando PyMuPDF Story."""
    kwargs: dict = {"html": html}
    if archive:
        kwargs["archive"] = archive
    user_css = _css_pdf(archive)
    if user_css:
        kwargs["user_css"] = user_css
    story = fitz.Story(**kwargs)
    buffer = io.BytesIO()
    writer = fitz.DocumentWriter(buffer)
    mediabox = fitz.paper_rect("a4")
    where = mediabox + (28, 28, -28, -28)
    while True:
        device = writer.begin_page(mediabox)
        more, _ = story.place(where)
        if not story.draw(device):
            writer.end_page()
            break
        writer.end_page()
    writer.close()
    return buffer.getvalue()


def combinar_pdf_orden(html: str, adjunto_path: str | None = None, archive: str | None = None) -> bytes:
    """PDF principal desde HTML + páginas del adjunto si existe."""
    principal = fitz.open(stream=html_a_pdf_bytes(html, archive), filetype="pdf")
    if adjunto_path and os.path.isfile(adjunto_path):
        try:
            adjunto = fitz.open(adjunto_path)
            principal.insert_pdf(adjunto)
            adjunto.close()
        except Exception:
            pass
    data = principal.tobytes()
    principal.close()
    return data
