"""Permisos de acceso por usuario a módulos de la aplicación."""
from __future__ import annotations

# Módulos de la portada / app
ALL_MODULOS = frozenset({
    "dashboard",
    "aldipod",
    "caja",              # Contados
    "caja_reembolsos",
    "presupuestos",
    "ordenes_carga",
    "llegadas",
    "rectificaciones",
    "vacaciones",
    "email",
    "ftp",
    "ficheros",
    "manager",
})

# '*' = acceso total
PERMISOS_USUARIO = {
    "jmurillo": frozenset({"*"}),
    "rocio": frozenset({"*"}),
    "pserrano": frozenset({"*"}),
    "javimurillo": frozenset({"*"}),
    "jamurillo": frozenset({"*"}),  # alias histórico
    "padiaz": frozenset({"rectificaciones", "aldipod"}),
    "fbonilla": frozenset({"rectificaciones", "aldipod", "caja", "presupuestos"}),
    "icastro": frozenset({
        "presupuestos",
        "ordenes_carga",
        "llegadas",
        "vacaciones",
        "rectificaciones",
    }),
    "mgallego": frozenset({"llegadas", "caja_reembolsos", "aldipod"}),
    "bgarcia": frozenset({"llegadas", "caja_reembolsos", "aldipod"}),
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
        "/editar_usuario",
        "/form_editar_usuario",
    ),
    "email": ("/email_destinatarios",),
    "ftp": ("/ftp_transfer",),
    "ficheros": ("/ficheros",),
}

RUTAS_SIEMPRE = frozenset({
    "/",
    "/portada",
    "/login",
    "/logout",
})


def _norm(username: str | None) -> str:
    return (username or "").strip().lower()


def acceso_total(username: str | None) -> bool:
    u = _norm(username)
    return u in PERMISOS_USUARIO and "*" in PERMISOS_USUARIO[u]


def tiene_restriccion(username: str | None) -> bool:
    """True si el usuario tiene ACL limitada (no acceso total)."""
    u = _norm(username)
    if u not in PERMISOS_USUARIO:
        return False
    return "*" not in PERMISOS_USUARIO[u]


def permisos_usuario(username: str | None) -> frozenset[str] | None:
    """
    Devuelve el set de módulos permitidos.
    None = sin ACL especial o acceso total (comportamiento sin filtro de portada restringida).
    Para acceso total también se devuelve ALL_MODULOS para pintar toda la portada.
    """
    u = _norm(username)
    if u not in PERMISOS_USUARIO:
        return None
    p = PERMISOS_USUARIO[u]
    if "*" in p:
        return ALL_MODULOS
    return frozenset(p)


def puede(username: str | None, modulo: str) -> bool:
    if acceso_total(username):
        return True
    p = permisos_usuario(username)
    if p is None:
        return True  # sin restricción explícita
    return modulo in p


def _path_cubre(path: str, prefix: str) -> bool:
    if path == prefix:
        return True
    if prefix.endswith("/"):
        return path.startswith(prefix)
    return path.startswith(prefix + "/")


def ruta_permitida(username: str | None, path: str) -> bool:
    """Comprueba si un path está permitido para el usuario (si tiene ACL limitada)."""
    if acceso_total(username):
        return True
    if not tiene_restriccion(username):
        return True

    p = permisos_usuario(username) or frozenset()
    path = path or "/"
    if path in RUTAS_SIEMPRE or path.startswith("/static/"):
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
