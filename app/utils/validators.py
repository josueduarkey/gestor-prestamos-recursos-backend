ALLOWED_EMAIL_DOMAIN = "@keytest.edu.sv"
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_UPLOAD_SIZE_MB = 5


def is_institutional_email(email: str) -> bool:
    return email.endswith(ALLOWED_EMAIL_DOMAIN)
