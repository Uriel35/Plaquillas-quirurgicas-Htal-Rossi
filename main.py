# -*- coding: utf-8 -*-
import os
import sys
import io
import subprocess
import locale
from datetime import datetime

import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from reportlab.platypus import TableStyle
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

import utils.run_console_utils as console_utils, utils.email_utils as email_utils, utils.main_utils as main_utils
import style.style as estilos

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller
    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ------------------ Adquirir data ------------------
def input_multilinea_df():
    print("Pegá los datos y presioná Enter dos veces:\n")

    columnas = [
        "Fecha", "Hora", "Edad", "DNI", "Sexo", "Nombre y apellido",
        "Diagnostico", "Sector", "Cirugia", " ",
        "Insumos", "SVE",
        "Cirujano", "Ayudante", "Localidad", "Obra social", "Nombre obra social"
    ]

    lineas = []
    while True:
        linea = input()
        if linea == "":
            break
        lineas.append(linea)

    texto = "\n".join(lineas)

    try:
        df = pd.read_csv(io.StringIO(texto), sep="\t", header=None)
        df = df.iloc[:, :len(columnas)]
        df.columns = columnas
    except Exception:
        console_utils.print_ANSI("El texto que copiaste NO es valido", "rojo")
        console_utils.print_ANSI("Volveras al menu", "rojo")
        return pd.DataFrame({})

    def poner_obra_social(x):
        if not pd.isna(x["Nombre obra social"]):
            x["Obra social"] = x["Nombre obra social"]
        return x
    # Limpieza
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df["Obra social"] = df["Obra social"].fillna("NO")
    df = df.apply(poner_obra_social, axis=1)
    df["Edad"] = df["Edad"].astype("Int64")

    cols_obj = df.select_dtypes(include="object").columns
    df[cols_obj] = df[cols_obj].fillna(" ")

    # Columnas extra
    df["Hab"] = "Amb"
    df["A"] = "L+N"
    df["I"] = "SI"
    df["T.Q"] = "M"
    return df


# ------------------ PDF ------------------

def generar_pdf(df, fecha_dt, turno, path_pdf):
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        path_pdf,
        pagesize=landscape(A4),
        leftMargin=20,
        rightMargin=20,
        topMargin=40,
        bottomMargin=20
    )

    final_df = df[[
        "DNI", "Nombre y apellido", "Edad", "Hab",
        "Obra social", "Diagnostico", "Cirugia",
        "Cirujano", "Ayudante", "A", "I", "T.Q"
    ]].rename(columns={"Obra social": "OOSS"})
    final_df = final_df.astype("string").fillna(" ")

    elements = []

    # Texto
    elements.extend([
        Paragraph("Reserva de turnos de Quirófano", estilos.titulo_style),
        Spacer(1, 12),
        Paragraph("Servicio de oftalmología de Htal Rossi de La Plata.", estilos.subtitulo_style),
        Spacer(1, 20),
        Paragraph(f"Fecha: {fecha_dt.strftime('%d/%m/%y')}.", styles["Normal"]),
        Paragraph(f"Día: {fecha_dt.strftime('%A').capitalize()} (Turno {turno}).", styles["Normal"]),
        Spacer(1, 20),
    ])

    # Tabla
    data = [final_df.columns.tolist()] + final_df.values.tolist()
    table = Table(data)

    table.setStyle(estilos.tabla_style)
    table_fontsize = main_utils.calcular_table_fontsize(final_df)
    table.setStyle(TableStyle([("FONTSIZE", (0, 0), (-1, -1), table_fontsize), ]))
    elements.append(table)

    # Build PDF + Logo
    doc.build(elements, onFirstPage=main_utils.agregar_logo)


# ------------------ Excel ------------------

def editar_excel(df):
    path_dir = os.path.join(str(main_utils.get_work_dir()), "data")
    path = os.path.join(path_dir, "excel.xlsx")
    os.makedirs(path_dir, exist_ok=True)
    df.to_excel(path, index=False)
    main_utils.abrir_archivo(path)
    while not console_utils.confirm_operation_y_or_n("Terminaste de editar el excel?"):
        pass
    df_modificado = pd.read_excel(path)
    df_modificado["Edad"] = df_modificado["Edad"].astype("Int64")
    # df_modificado["Edad"] = (
    #     df_modificado["Edad"]
    #     .replace(" ", pd.NA)
    #     .astype("Int64")
    # )
    return df_modificado


# ------------------ Main ------------------

def main():
    main_utils.set_locale()

    df = pd.DataFrame({})
    fecha_dt = datetime.today()
    turno = main_utils.calcular_turno(fecha_dt)

    pdf_path = os.path.join(str(main_utils.get_work_dir()), "plantilla_quirofano.pdf")

    def cargar():
        nonlocal df, fecha_dt, turno
        df = input_multilinea_df()
        if df.empty: return
        f = main_utils.detectar_fecha(df)
        if f:
            fecha_dt = f
            turno = main_utils.calcular_turno(f)

    def crear_pdf():
        if df.empty:
            console_utils.print_ANSI("No hay datos", "rojo")
            return
        generar_pdf(df, fecha_dt, turno, path_pdf=pdf_path)
        visualizar_pdf()
        input("Visualizando vista previa de PDF. Enter para continuar")

        if console_utils.confirm_operation_y_or_n("Queres enviarlo por email?"):
            enviar_pdf_email()
            print("Mensaje enviado")


    def editar_fecha():
        nonlocal fecha_dt, turno
        console_utils.print_ANSI(f"Fecha actual: {fecha_dt.strftime('%d/%m/%y')}")
        while True:
            try:
                nueva = input("Fecha dd/mm/aa: ")
                fecha_dt = datetime.strptime(nueva, "%d/%m/%y")
                turno = main_utils.calcular_turno(fecha_dt)
                break
            except:
                print("Formato inválido")

    def editar_turno():
        nonlocal turno
        console_utils.print_ANSI(f"Turno actual: {turno} ", "amarillo")
        turno = console_utils.option_menu_mkr(["Mañana", "Tarde"], "Turno:")

    def editar_df():
        nonlocal df
        df = editar_excel(df)

    def visualizar_pdf():
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.run(['open', pdf_path])
        elif os.name == 'nt':  # Windows
            os.startfile(pdf_path)
        elif os.name == 'posix':  # Linux
            subprocess.run(['xdg-open', pdf_path])
        else:
            raise OSError('Sistema operativo no soportado')
        return

    def enviar_pdf_email():
        nonlocal pdf_path
        to = "drluciaolivera@gmail.com"
        body_mensaje = f"""
        Envio adjunto el PDF de la  reserva de quirófanos de la fecha {fecha_dt.strftime('%d-%m-%y')}.
        Saludos
        """
        nombre_archivo = f"{fecha_dt.strftime('%d-%m-%y')}_quirofano_oftalmologia"
        email_utils.enviar_mail(to=to, subject=f"Reserva de quirofanos {fecha_dt.strftime('%d-%m-%y')}", body=body_mensaje, pdf_path=pdf_path, nombre_pdf=nombre_archivo)
        return

    menu = {
        "Cargar datos": cargar,
        "Ver tabla": lambda: print(df),
        "Editar Excel": editar_df,
        "Crear PDF": crear_pdf,
        "Editar fecha": editar_fecha,
        "Editar turno": editar_turno,
        "Visualizar PDF": visualizar_pdf,
        "Enviar PDF a email": enviar_pdf_email,
    }

    while console_utils.menu_start_mkr(menu, "¿Qué querés hacer?"):
        pass


if __name__ == "__main__":
    main()
