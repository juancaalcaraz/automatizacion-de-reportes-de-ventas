from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from datetime import datetime
import os

def generate_pdf(kpis, figures_dir, output_path):
    """
    Genera un PDF ejecutivo tipo dashboard:
    - KPIs destacados (una fila, varias columnas)
    - Gráficos: ventas totales, medios de pago, serie histórica
    - Footer con fuente de datos
    """
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    elements = []

    # --- Header ---
    elements.append(Paragraph("Reporte Ejecutivo – Ventas en Supermercados", styles['Title']))
    elements.append(Paragraph(f"Actualización: {datetime.today().strftime('%d/%m/%Y')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # --- KPIs ---
    elements.append(Paragraph("Indicadores Clave", styles['Heading2']))
    # El DF tiene una fila con múltiples columnas
    kpi_data = [[col, f"{kpis.loc[0, col]:,.2f}"] for col in kpis.columns if isinstance(kpis.loc[0, col], (int, float))]
    table = Table(kpi_data, colWidths=[10*cm, 5*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),colors.lightblue),
        ('TEXTCOLOR',(0,0),(-1,0),colors.black),
        ('GRID',(0,0),(-1,-1),1,colors.grey),
        ('FONTNAME',(0,0),(-1,-1),'Helvetica-Bold'),
        ('ALIGN',(1,0),(-1,-1),'RIGHT')
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # --- Insertar gráficos ---
    img_files = ["ventas_totales.png", "medios_pago.png", "serie_historica.png"]
    titles = ["Ventas Totales Mensuales", "Distribución de Medios de Pago", "Ventas por Categoría"]

    for title, img_file in zip(titles, img_files):
        img_path = os.path.join(figures_dir, img_file)
        if os.path.exists(img_path):
            elements.append(Paragraph(title, styles['Heading2']))
            width = 16*cm if img_file != "medios_pago.png" else 12*cm
            height = 8*cm
            elements.append(Image(img_path, width=width, height=height))
            elements.append(Spacer(1,12))
        else:
            elements.append(Paragraph(f"Gráfico '{title}' no disponible.", styles['Italic']))

    # --- Footer ---
    elements.append(Spacer(1, 24))
    elements.append(Paragraph(
        "Fuente: INDEC – Datos Abiertos Argentina. Reporte generado automáticamente.",
        styles['Italic']
    ))

    # --- Generar PDF ---
    doc.build(elements)
    print(f"✅ PDF ejecutivo generado en: {output_path}")
