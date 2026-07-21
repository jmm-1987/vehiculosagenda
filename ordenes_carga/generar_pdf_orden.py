"""PDF de orden de carga con Chromium (mismo motor que Imprimir) + fusión de adjuntos."""
from __future__ import annotations

import os
import re
from urllib.parse import unquote, urlparse

import fitz

_PDF_BASE = "http://orden-carga.local"
_PLAYWRIGHT_PATHS = ("/opt/playwright-browsers",)


def _configurar_playwright() -> None:
    """Usa navegadores instalados en ruta compartida del servidor (p. ej. www-data)."""
    if os.environ.get("PLAYWRIGHT_BROWSERS_PATH"):
        return
    for path in _PLAYWRIGHT_PATHS:
        if os.path.isdir(path) and os.access(path, os.R_OK | os.X_OK):
            os.environ["PLAYWRIGHT_BROWSERS_PATH"] = path
            return


def _inyectar_base(html: str) -> str:
    if re.search(r"<base\s", html, re.I):
        return html
    return re.sub(r"(<head[^>]*>)", rf'\1<base href="{_PDF_BASE}/">', html, count=1, flags=re.I)


def _ruta_estatica_desde_url(url: str, static_dir: str) -> str | None:
    parsed = urlparse(url)
    path = unquote(parsed.path or "")
    marker = "/static/"
    idx = path.find(marker)
    if idx == -1:
        return None
    rel = path[idx + len(marker) :].lstrip("/").replace("/", os.sep)
    if not rel or ".." in rel.split(os.sep):
        return None
    full = os.path.join(static_dir, rel)
    return full if os.path.isfile(full) else None


def imprimir_html_a_pdf(html: str, static_dir: str) -> bytes:
    """Renderiza el HTML de impresión con Chromium (CSS @media print, igual que el navegador)."""
    _configurar_playwright()
    from playwright.sync_api import sync_playwright

    html = _inyectar_base(html)
    static_dir = os.path.abspath(static_dir)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = browser.new_page()

        def _route(route):
            url = route.request.url
            local = _ruta_estatica_desde_url(url, static_dir)
            if local:
                route.fulfill(path=local)
                return
            route.continue_()

        page.route("**/*", _route)
        page.set_content(html, wait_until="networkidle", timeout=60_000)
        page.wait_for_timeout(400)
        pdf = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        )
        browser.close()
        return pdf


def combinar_pdf_orden(html: str, adjunto_path: str | None = None, static_dir: str | None = None) -> bytes:
    """Primera hoja = impresión Chromium; páginas siguientes = PDF adjunto."""
    if not static_dir:
        raise ValueError("static_dir es obligatorio para generar el PDF")
    principal = fitz.open(stream=imprimir_html_a_pdf(html, static_dir), filetype="pdf")
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
