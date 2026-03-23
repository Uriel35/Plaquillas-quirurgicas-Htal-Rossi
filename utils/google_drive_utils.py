from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
import os

# DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.file"]
DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def login_drive():
    token_path = "./google_drive/token.json"
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(token_path)
    gauth.settings['get_refresh_token'] = True  # 🔑 Esto es importante

    if gauth.credentials is None:
        gauth.LoadClientConfigFile('./google_drive/client_secrets.json')
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile(token_path)  # Guarda el token para futuros usos
    elif gauth.access_token_expired:
        try:
            gauth.LoadClientConfigFile('./google_drive/client_secrets.json')
            gauth.Refresh()
            gauth.SaveCredentialsFile(token_path)
        except Exception as error:
            input("Refresh token ha sido caducado. Procedo a eliminar token.json")
            os.remove(token_path)
            input("Se elimino token.json. Reinicio funcion")
            return False
    else:
        gauth.Authorize()
    return gauth


def create_drive_text(nombre, contenido, id_folder):
    credentials = login_drive()
    if not credentials:
        credentials = login_drive()
    file = credentials.CreateFile({
        "title": nombre,
        "parents": [{"kind": "drive#fileLink", "id": id_folder}]
    })
    file.SetContentString(contenido)
    file.Upload()
    return


def download_file_as_csv(id, path, name):
    gauth = login_drive()
    if not gauth:
        gauth = login_drive()
    drive = GoogleDrive(gauth)
    file = drive.CreateFile({'id': id})
    file.GetContentFile(os.path.join(path, name + '.csv'), mimetype='text/csv')


def authenticate_drive():
    creds = None
    token_path = "./drive_credentials/drive_token_drive.json"
    client_secrets_path = "./drive_credentials/drive_client_secrets.json"

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, DRIVE_SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Renovar token de acceso
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, DRIVE_SCOPES)
            creds = flow.run_local_server(port=0)  # Inicia autenticación en navegador
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    return build("drive", "v3", credentials=creds)
