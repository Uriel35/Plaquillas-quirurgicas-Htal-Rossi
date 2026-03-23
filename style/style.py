from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Image
from reportlab.lib.pagesizes import A4, landscape

styles = getSampleStyleSheet()

titulo_style = ParagraphStyle(
    name="TituloCustom",
    parent=styles["Title"],
    fontSize=20,
    leading=24,
    alignment=TA_CENTER,
    underline=True,
    spaceAfter=10
)

subtitulo_style = ParagraphStyle(
    name="SubtituloCustom",
    parent=styles["Normal"],
    fontSize=14,
    leading=18,
    alignment=TA_CENTER,
    spaceAfter=6,
    fontName="Helvetica-Bold"
)

header_color = colors.HexColor("#71ACC2")
tabla_style = TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), header_color),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
])
