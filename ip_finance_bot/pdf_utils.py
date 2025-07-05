from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def generate_pdf(transactions, file_path="report.pdf"):
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Финансовый отчёт")
    c.setFont("Helvetica", 12)

    y = height - 80
    for t in transactions:
        line = f"{t.created_at.strftime('%Y-%m-%d')} | {t.type.upper():7} | {t.amount:>8.2f} | {t.category or '—'} | {t.description or '—'}"
        c.drawString(30, y, line)
        y -= 18
        if y < 50:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 12)

    c.save()
    return file_path
