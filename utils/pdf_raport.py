from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors


def generate_pdf_report(
    output_path,
    aktualny_sygnal,
    srednie_rr,
    sdnn,
    min_rr,
    max_rr,
    liczba_r,
    threshold_rr,
    distance_rr,
    signal_duration,
    sample_count,
    analysis_start,
    analysis_end
):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    styles['Title'].fontName = 'Helvetica'
    styles['Normal'].fontName = 'Helvetica'
    styles['Heading2'].fontName = 'Helvetica'


    styles['Title'].fontSize = 18
    styles['Heading2'].fontSize = 13
    styles['Normal'].fontSize = 11

    elements = []

    title = Paragraph(
        "Raport z analizy HRV sygnału EKG",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 8))

    date_text = Paragraph(
        f"Data wygenerowania: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        styles['Normal']
    )

    elements.append(date_text)
    elements.append(Spacer(1, 10))

    signal_text = Paragraph(
        f"Badany sygnał: {aktualny_sygnal}",
        styles['Normal']
    )
    elements.append(signal_text)
    elements.append(Spacer(1, 8))

    info_title = Paragraph(
        "Informacje o analizie",
        styles['Heading2']
    )

    elements.append(info_title)
    elements.append(Spacer(1, 10))

    info_data = [
        f"Długość sygnału: {signal_duration:.1f} s",
        f"Liczba próbek: {sample_count}",
        f"Zakres analizy: {analysis_start:.1f} s - {analysis_end:.1f} s"
    ]

    for info in info_data:

        elements.append(
            Paragraph(info, styles['Normal'])
        )

        elements.append(Spacer(1, 6))

    elements.append(Spacer(1, 10))

    

    analysis_title = Paragraph(
        "Parametry analizy",
        styles['Heading2']
    )

    elements.append(analysis_title)
    elements.append(Spacer(1, 10))

    analysis_params = [
        f"Próg detekcji R: {threshold_rr}",
        f"Minimalny dystans RR: {distance_rr} ms"
    ]

    for param in analysis_params:

        elements.append(
            Paragraph(param, styles['Normal'])
        )

        elements.append(Spacer(1, 6))

    elements.append(Spacer(1, 10))

    stats_title = Paragraph(
        "Statystyki HRV",
        styles['Heading2']
    )

    elements.append(stats_title)
    elements.append(Spacer(1, 10))

    table_data = [
        ["Parametr", "Wartość"],

        ["Średnie RR", f"{srednie_rr:.0f} ms"],

        ["SDNN", f"{sdnn:.0f} ms"],

        ["Min RR", f"{min_rr:.0f} ms"],

        ["Max RR", f"{max_rr:.0f} ms"],

        ["Liczba załamków R", f"{liczba_r:.0f}"]
    ]

    table = Table(
        table_data,
        colWidths=[220, 180]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#444444')),

        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),

        ('FONTSIZE', (0, 0), (-1, -1), 12),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),

        ('GRID', (0, 0), (-1, -1), 1, colors.grey),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))

    elements.append(table)
    elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 8))

    sync_title = Paragraph(
        "Analiza synchronizacji fazowej",
        styles['Heading2']
    )

    elements.append(sync_title)
    elements.append(Spacer(1, 10))

    sync_description = """

    Zaobserwowano zależność pomiędzy rytmem serca
    a fazą sygnału oddechowego. Analiza synchrogramu
    umożliwia ocenę synchronizacji fazowej pomiędzy
    rytmem serca i oddechem.

    """

    elements.append(
        Paragraph(sync_description, styles['Normal'])
    )

    elements.append(Spacer(1, 10))

    summary_title = Paragraph(
        "Wnioski",
        styles['Heading2']
    )

    elements.append(summary_title)
    elements.append(Spacer(1, 10))

    summary = []

    if sdnn < 50:

        summary.append(
            "Zaobserwowano obniżoną zmienność rytmu serca (HRV)."
        )

    else:

        summary.append(
            "Zmienność rytmu serca (HRV) mieści się w prawidłowym zakresie."
        )

    if srednie_rr < 700:

        summary.append(
            "Średnia wartość RR wskazuje na podwyższoną częstość rytmu serca."
        )

    else:

        summary.append(
            "Średnia wartość RR wskazuje na stabilny rytm serca."
        )

    summary.append(
        "Analiza została wykonana automatycznie na wybranym fragmencie sygnału."
    )

    for text in summary:

        elements.append(
            Paragraph(f"• {text}", styles['Normal'])
        )

        elements.append(Spacer(1, 8))

    elements.append(Spacer(1, 8))

    footer = Paragraph(
        "Raport wygenerowano automatycznie w aplikacji do analizy HRV sygnału EKG.",
        styles['Normal']
    )

    elements.append(footer)

    doc.build(elements)