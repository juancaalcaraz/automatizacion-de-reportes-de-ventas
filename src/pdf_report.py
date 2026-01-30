from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from datetime import datetime
import os
import PyPDF2

def generate_pdf(kpis, forecast_df, figures_dir, output_path):
    """
    Genera un PDF ejecutivo incluyendo la tabla de escenarios.
    """
    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        rightMargin=1.5*cm, leftMargin=1.5*cm,
        topMargin=1.5*cm, bottomMargin=1.5*cm
    )

    styles = getSampleStyleSheet()
    # Estilo personalizado para celdas de tabla
    style_table_header = styles['Normal']
    elements = []

    # --- Header ---
    elements.append(Paragraph("Reporte Ejecutivo – Análisis de Ventas y Proyecciones", styles['Title']))
    elements.append(Paragraph(f"Fecha de emisión: {datetime.today().strftime('%d/%m/%Y')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # --- KPIs Destacados ---
    elements.append(Paragraph("Indicadores Clave de Desempeño (KPIs)", styles['Heading2']))
    kpi_data = [[col, f"{kpis.loc[0, col]:,.2f}"] for col in kpis.columns if isinstance(kpis.loc[0, col], (int, float))]
    
    table_kpi = Table(kpi_data, colWidths=[10*cm, 6*cm])
    table_kpi.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), colors.whitesmoke),
        ('GRID',(0,0),(-1,-1), 0.5, colors.grey),
        ('FONTNAME',(0,0),(-1,-1), 'Helvetica-Bold'),
        ('ALIGN',(1,0),(-1,-1), 'RIGHT'),
        ('LEFTPADDING', (0,0), (-1,-1), 10)
    ]))
    elements.append(table_kpi)
    elements.append(Spacer(1, 15))

    # --- Sección de Proyecciones ---
    elements.append(Paragraph("Pronóstico de Ventas Próximo Trimestre", styles['Heading2']))
    
    # Insertar el gráfico de escenarios que creamos antes
    img_path = os.path.join(figures_dir, "forecast_escenarios.png")
    if os.path.exists(img_path):
        elements.append(Image(img_path, width=17*cm, height=7.5*cm))
    
    elements.append(Spacer(1, 10))

    # --- Tabla de Escenarios (Lo que pediste) ---
    elements.append(Paragraph("Detalle de Escenarios Probabilísticos (Miles de Millones)", styles['Heading3']))
    
    # Preparamos los datos para la tabla del PDF
    # Tomamos el forecast_df que ya tiene las columnas: Mes, Escenario Mínimo (B), Proyección Base (B), Escenario Máximo (B)
    header = ["Mes", "E. Mínimo", "E. Base", "E. Máximo"]
    table_data = [header] + forecast_df[["Mes", "Ventas Escenario Mínimo", "Proyección Ventas (Base)", "Ventas Escenario Máximo"]].values.tolist()

    table_forecast = Table(table_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    table_forecast.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#2c3e50")), # Azul oscuro corporativo
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.whitesmoke]) # Filas cebra
    ]))
    elements.append(table_forecast)
    elements.append(Spacer(1, 15))
    """
    # --- Insertar gráficos ---
    img_files = [ "medios_pago.png", "serie_historica.png"]
    titles = ["Distribución de Medios de Pago", "Ventas por Categoría"]

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
     """
    # --- Footer ---
    elements.append(Paragraph(
        "Este reporte utiliza modelos predictivos basados en suavizamiento exponencial (Holt-Winters). "
        "Los escenarios representan un intervalo de confianza del 95%.",
        styles['Italic']
    ))

    doc.build(elements)
    print(f"✅ Dashboard PDF generado exitosamente en: {output_path}.")

def protect_pdf(input_path, output_path, password):
    """
    Funcion para proteger el pdf. 
    """
    try:
        reader = PyPDF2.PdfReader(input_path)
        writer = PyPDF2.PdfWriter()

        # Copiar todas las páginas al escritor
        for page in reader.pages:
            writer.add_page(page)

        # Aplicar la encriptación
        writer.encrypt(password)

        # Guardar el archivo protegido
        with open(output_path, "wb") as f:
            writer.write(f)
        
        print(f"🔒 PDF protegido exitosamente: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error al proteger el PDF: {e}")
        return False
