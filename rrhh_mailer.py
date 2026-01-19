"""
Módulo aislado para enviar por correo los datos de un formulario de RRHH.

La función principal `enviar_formulario_rrhh` acepta un diccionario con los
datos del formulario y, opcionalmente, el fichero PDF del currículum. Envía un
correo desde `rrhh@alditraex.es` hacia `jmurillo@alditraex.es` usando los
parámetros SMTP definidos por variables de entorno o por el argumento
`smtp_config`.
"""

from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import BinaryIO, Mapping, MutableMapping, Optional, Union

# Correos por defecto solicitados por el usuario.
DEFAULT_SENDER = "rrhh@alditraex.es"
DEFAULT_RECIPIENT = "info@alditraex.es"

# Campos mínimos esperados en el formulario mostrado en la captura.
REQUIRED_FIELDS = {
    "nombre_completo": "Nombre completo",
    "correo_electronico": "Correo electrónico",
    "telefono": "Teléfono",
    "area_interes": "Área de interés",
    "presentacion": "Breve presentación",
}


class ConfiguracionSMTPError(RuntimeError):
    """Se lanza cuando falta información esencial para el envío SMTP."""


def _leer_archivo(file_obj: Union[BinaryIO, bytes, bytearray]) -> tuple[bytes, str]:
    """Devuelve el contenido binario y el nombre de un archivo adjunto."""
    if file_obj is None:
        raise ValueError("No se proporcionó un archivo para adjuntar.")

    if isinstance(file_obj, (bytes, bytearray)):
        return bytes(file_obj), "curriculum.pdf"

    if hasattr(file_obj, "read"):
        contenido = file_obj.read()
        # Volvemos al inicio por si el objeto se reutiliza después
        if hasattr(file_obj, "seek"):
            file_obj.seek(0)
        nombre = getattr(file_obj, "filename", "curriculum.pdf") or "curriculum.pdf"
        return contenido, nombre

    raise TypeError("El tipo del archivo proporcionado no es soportado.")


def _resolver_configuracion(
    smtp_config: Optional[MutableMapping[str, Union[str, int, bool]]] = None,
) -> dict:
    """Obtiene la configuración SMTP combinando argumentos y variables de entorno."""
    # Puerto 465 normalmente usa SSL, puerto 587 usa TLS
    port_default = int(os.getenv("SMTP_PORT", "465"))
    use_ssl_default = str(os.getenv("SMTP_USE_SSL", "")).lower()
    use_tls_default = str(os.getenv("SMTP_USE_TLS", "")).lower()
    
    # Si no se especifica, inferir según el puerto
    if not use_ssl_default and not use_tls_default:
        use_ssl_default = "true" if port_default == 465 else "false"
        use_tls_default = "true" if port_default == 587 else "false"
    
    config = {
        "host": os.getenv("SMTP_HOST", "smtp.ionos.es"),
        "port": port_default,
        "user": os.getenv("SMTP_USER", "rrhh@alditraex.es"),
        "password": os.getenv("SMTP_PASSWORD", "RRHH.b06422208"),
        "use_tls": use_tls_default == "true",
        "use_ssl": use_ssl_default == "true",
        "sender": os.getenv("RRHH_FORM_SENDER", DEFAULT_SENDER),
        "recipient": os.getenv("RRHH_FORM_RECIPIENT", DEFAULT_RECIPIENT),
    }

    if smtp_config:
        config.update(smtp_config)

    if not config["host"]:
        raise ConfiguracionSMTPError("SMTP_HOST no está configurado.")
    if not config["port"]:
        raise ConfiguracionSMTPError("SMTP_PORT no está configurado.")
    if config.get("use_tls") and config.get("use_ssl"):
        raise ConfiguracionSMTPError("Seleccione solo TLS o SSL, no ambos.")

    # Normalizamos tipos
    config["port"] = int(config["port"])
    config["use_tls"] = bool(config["use_tls"])
    config["use_ssl"] = bool(config["use_ssl"])

    return config


def _validar_formulario(datos: Mapping[str, str]) -> None:
    faltantes = [etiqueta for clave, etiqueta in REQUIRED_FIELDS.items() if not datos.get(clave)]
    if faltantes:
        raise ValueError(
            f"Faltan campos obligatorios en el formulario: {', '.join(faltantes)}"
        )


def enviar_formulario_rrhh(
    datos_formulario: Mapping[str, str],
    curriculum_pdf: Optional[Union[BinaryIO, bytes, bytearray]] = None,
    smtp_config: Optional[MutableMapping[str, Union[str, int, bool]]] = None,
) -> None:
    """
    Envía por email la información del formulario de RRHH.

    Parameters
    ----------
    datos_formulario:
        Diccionario con los campos del formulario. Se esperan las claves
        definidas en REQUIRED_FIELDS (`nombre_completo`, `correo_electronico`,
        `telefono`, `area_interes`, `presentacion`). Se pueden incluir campos
        adicionales; se añadirán automáticamente al cuerpo del correo.
    curriculum_pdf:
        Archivo PDF opcional (objeto FileStorage de Flask, file-like, bytes o
        bytearray) que se adjuntará al correo.
    smtp_config:
        Configuración SMTP opcional para sobrescribir variables de entorno.
        Acepta las claves: host, port, user, password, use_tls, use_ssl,
        sender, recipient.
    """
    _validar_formulario(datos_formulario)
    config = _resolver_configuracion(smtp_config)

    mensaje = EmailMessage()
    mensaje["From"] = config.get("sender", DEFAULT_SENDER)
    mensaje["To"] = config.get("recipient", DEFAULT_RECIPIENT)
    mensaje["Subject"] = f"Nuevo formulario web - {datos_formulario['nombre_completo']}"

    lineas = [
        "Se ha recibido un nuevo formulario desde la web:",
        "",
    ]
    for clave, etiqueta in REQUIRED_FIELDS.items():
        lineas.append(f"{etiqueta}: {datos_formulario.get(clave, '')}")

    # Campos adicionales
    extras = {
        clave: valor for clave, valor in datos_formulario.items() if clave not in REQUIRED_FIELDS
    }
    if extras:
        lineas.append("")
        lineas.append("Campos extra:")
        for clave, valor in extras.items():
            lineas.append(f"- {clave}: {valor}")

    mensaje.set_content("\n".join(lineas))

    if curriculum_pdf:
        contenido, nombre = _leer_archivo(curriculum_pdf)
        mensaje.add_attachment(
            contenido,
            maintype="application",
            subtype="pdf",
            filename=nombre,
        )

    if config.get("use_ssl"):
        smtp_cls = smtplib.SMTP_SSL
    else:
        smtp_cls = smtplib.SMTP

    with smtp_cls(config["host"], config["port"]) as servidor:
        if config.get("use_tls"):
            servidor.starttls()
        if config.get("user") and config.get("password"):
            servidor.login(config["user"], config["password"])
        servidor.send_message(mensaje)


__all__ = ["enviar_formulario_rrhh", "ConfiguracionSMTPError"]

