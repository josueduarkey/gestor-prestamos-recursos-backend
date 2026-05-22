import logging
from pathlib import Path
from typing import Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config.settings import settings

logger = logging.getLogger(__name__)

_mail_config: Optional[ConnectionConfig] = None
_fast_mail: Optional[FastMail] = None


def _get_fast_mail() -> Optional[FastMail]:
    global _mail_config, _fast_mail
    if not settings.MAILTRAP_USER or not settings.MAILTRAP_PASSWORD:
        return None
    if _fast_mail is None:
        _mail_config = ConnectionConfig(
            MAIL_USERNAME=settings.MAILTRAP_USER,
            MAIL_PASSWORD=settings.MAILTRAP_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_PORT=settings.MAILTRAP_PORT,
            MAIL_SERVER=settings.MAILTRAP_HOST,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates" / "emails",
        )
        _fast_mail = FastMail(_mail_config)
    return _fast_mail


async def _send(subject: str, recipient: str, template: str, context: dict) -> None:
    fm = _get_fast_mail()
    if not fm:
        logger.warning("Email not configured — skipping %s to %s", template, recipient)
        return
    try:
        logo_path = Path(__file__).parent.parent.parent / "logo-key.png"
        message = MessageSchema(
            subject=subject,
            recipients=[recipient],
            template_body=context,
            subtype=MessageType.html,
            attachments=[logo_path] if logo_path.exists() else [],
        )
        await fm.send_message(message, template_name=template)
        logger.info("Email sent: %s → %s", template, recipient)
    except Exception as exc:
        logger.error("Failed to send %s to %s: %s", template, recipient, exc)


async def send_loan_created_email(recipient: str, context: dict) -> None:
    await _send(
        subject="Préstamo registrado — Key Institute",
        recipient=recipient,
        template="loan_created.html",
        context=context,
    )


async def send_loan_overdue_email(recipient: str, context: dict) -> None:
    await _send(
        subject="⚠️ Tienes un préstamo vencido — Key Institute",
        recipient=recipient,
        template="loan_overdue.html",
        context=context,
    )


async def send_printing_3d_email(recipient: str, context: dict) -> None:
    await _send(
        subject="Solicitud de impresión 3D registrada — Key Institute",
        recipient=recipient,
        template="printing_3d_created.html",
        context=context,
    )
