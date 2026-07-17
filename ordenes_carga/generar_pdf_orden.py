"""Convierte HTML de impresión a PDF y fusiona adjuntos con PyMuPDF."""
from __future__ import annotations

import io
import os

import fitz


def html_a_pdf_bytes(html: str, archive: str | None = None) -> bytes:
    """Renderiza HTML a PDF A4 usando PyMuPDF Story."""
    kwargs = {"html": html}
    if archive:
        kwargs["archive"] = archive
    story = fitz.Story(**kwargs)
    buffer = io.BytesIO()
    writer = fitz.DocumentWriter(buffer)
    mediabox = fitz.paper_rect("a4")
    where = mediabox + (36, 36, -36, -36)
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
