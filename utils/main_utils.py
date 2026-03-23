import pandas as pd
import os
import sys
import subprocess
import locale
from datetime import datetime

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def calcular_col_widths(df, page_width, min_width=40, max_width=None):
    """
    Calcula anchos de columnas proporcionales al contenido,
    garantizando que la suma == page_width.
    """

    # ---- Largo máximo por columna (incluye headers)
    max_chars_col = pd.concat([
        df.astype(str).map(len),
        pd.DataFrame([df.columns.map(len)], columns=df.columns)
    ]).max()

    total_chars = max_chars_col.sum()

    # ---- Evitar división por 0
    if total_chars == 0:
        return [page_width / len(df.columns)] * len(df.columns)

    # ---- Proporción inicial
    col_widths = [
        (chars / total_chars) * page_width
        for chars in max_chars_col
    ]

    # ---- Aplicar mínimos y máximos
    adjusted = []
    for w in col_widths:
        if min_width:
            w = max(w, min_width)
        if max_width:
            w = min(w, max_width)
        adjusted.append(w)

    col_widths = adjusted

    # ---- 🔴 NORMALIZACIÓN FINAL (CLAVE)
    scale = page_width / sum(col_widths)
    col_widths = [w * scale for w in col_widths]

    return col_widths



def calcular_table_fontsize(df):
    max_chars_col = df.astype(str).map(len).max()
    total_chars = max_chars_col.sum()
    if total_chars > 130:
        table_fontsize = 6
    elif total_chars > 115:
        table_fontsize = 7
    elif total_chars > 100:
        table_fontsize = 8
    elif total_chars > 80:
        table_fontsize = 9
    else:
        table_fontsize = 11
    return table_fontsize


def agregar_logo(canvas, doc):
    logo_path = resource_path("data/htal_rossi_logo.png")
    width = 80
    height = 80
    x = doc.pagesize[0] - width - 40
    y = doc.pagesize[1] - height - 40
    canvas.drawImage(logo_path, x, y, width=width, height=height)


def abrir_archivo(path):
    try:
        if sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", path])
        elif sys.platform == "darwin":
            subprocess.run(["open", path])
        elif sys.platform == "win32":
            os.startfile(path)
    except Exception:
        pass



def set_locale():
    try:
        locale.setlocale(locale.LC_TIME, "es_AR.UTF-8")
    except:
        try:
            locale.setlocale(locale.LC_TIME, "Spanish_Argentina")
        except:
            pass

def detectar_fecha(df):
    for fecha in df["Fecha"]:
        try:
            return datetime.strptime(str(fecha), "%d/%m/%y")
        except:
            continue
    return None


def calcular_turno(fecha_dt):
    return "Tarde" if fecha_dt.weekday() == 2 else "Mañana"
