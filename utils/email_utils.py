import os
import base64
import sys
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Permiso para enviar mails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def resource_path(relative_path):
    """Para archivos incluidos en PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_work_dir(app_name: str = "Quirofano_oftalmologia_rossi") -> Path:
    """
    Carpeta escribible para tokens/archivos generados.
    En ejecutable portable usamos la carpeta del .exe; si no se puede, HOME.
    """
    if getattr(sys, "frozen", False):
        app_dir = Path(sys.executable).resolve().parent
    else:
        app_dir = Path(os.path.abspath("."))

    try:
        if os.access(app_dir, os.W_OK):
            return app_dir
    except Exception:
        pass

    fallback = Path.home() / app_name
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


def user_data_path(relative_path):
    """Para archivos que se crean/modifican (token)"""
    base_path = get_work_dir() / "credentials"
    base_path.mkdir(parents=True, exist_ok=True)
    return str(base_path / os.path.basename(relative_path))


def autenticar():
    creds = None

    token_path = user_data_path("email_token.json")
    creds_path = resource_path("credentials/email_credentials.json")

    # cargar token existente
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # refrescar o login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # guardar token SIEMPRE fuera del bundle
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return creds


def crear_mensaje(to, subject, body):
    mensaje = MIMEText(body)
    mensaje['to'] = to
    mensaje['subject'] = subject
    raw = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()
    return {'raw': raw}


def crear_mensaje_con_adjunto(to, subject, body, pdf_path, nombre_archivo=None):
    mensaje = MIMEMultipart()
    mensaje['to'] = to
    mensaje['subject'] = subject

    # cuerpo del mail
    mensaje.attach(MIMEText(body, 'plain'))

    # adjunto PDF
    with open(pdf_path, 'rb') as f:
        adjunto = MIMEApplication(f.read(), _subtype='pdf')
        if nombre_archivo is None:
            nombre_archivo = os.path.basename(pdf_path)
        adjunto.add_header(
            'Content-Disposition',
            'attachment',
            filename=nombre_archivo
        )
        mensaje.attach(adjunto)

    # encode base64
    raw = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()

    return {'raw': raw}


def enviar_mail(to, subject, body, pdf_path=None, nombre_pdf=None):
    creds = autenticar()
    service = build('gmail', 'v1', credentials=creds)

    if pdf_path:
        mensaje = crear_mensaje_con_adjunto(to, subject, body, pdf_path=pdf_path, nombre_archivo=nombre_pdf)
    else:
        mensaje = crear_mensaje(to, subject, body)

    enviado = service.users().messages().send(
        userId='me',
        body=mensaje
    ).execute()

    return enviado
