from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.contrib.auth import get_user_model
from .models import WorkEntry

User = get_user_model()

def generate_monthly_payroll_pdf(month, filename):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(filename, pagesize=A4)

    elements = []

    title = Paragraph(f"Monthly Payroll Report — {month}", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 20))

    users = User.objects.all()

    for user in users:
        work_entries = WorkEntry.objects.filter(
            user=user,
            date__startswith=month
        )

        if not work_entries.exists():
            continue

        elements.append(Paragraph(f"Employee: {user.username}", styles['Heading2']))

        table_data = [["Date", "Start", "End", "Hours"]]
        total_hours = 0

        for entry in work_entries:
            hours = entry.get_hours()
            total_hours += hours

            table_data.append([
                entry.date.strftime("%Y-%m-%d"),
                entry.start_time.strftime("%H:%M"),
                entry.end_time.strftime("%H:%M"),
                f"{hours:.2f}"
            ])

        table_data.append(["", "", "Total", f"{total_hours:.2f}"])

        table = Table(table_data, colWidths=[100, 100, 100, 100])
        table.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('BACKGROUND', (-2,-1), (-1,-1), colors.lightgrey),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 30))

    doc.build(elements)
