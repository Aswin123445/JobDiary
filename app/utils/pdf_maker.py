from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from datetime import datetime

def save_summary_to_pdf(summary_text, filename="job_application_report.pdf"):
    # Create the PDF document
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=20,
        leading=24,
        spaceAfter=20
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=14
    )

    elements = []

    # Report Title
    elements.append(Paragraph("📄 Job Application & Company Research Report", title_style))
    elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Italic']))
    elements.append(Spacer(1, 0.3 * inch))

    # AI Summary Body
    for paragraph in summary_text.split("\n\n"):
        if paragraph.strip():
            elements.append(Paragraph(paragraph.strip(), body_style))
            elements.append(Spacer(1, 0.2 * inch))

    # Build PDF
    doc.build(elements)
    print(f"✅ Report saved as {filename}")
