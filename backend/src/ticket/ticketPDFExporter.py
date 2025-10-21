from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

class TicketPDFExporter:
    def __init__(self, ticket, client):
        self.client = client
        self.ticket = ticket

    def generar_pdf(self):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=30, rightMargin=30, topMargin=30, bottomMargin=30)
        styles = getSampleStyleSheet()
        story = []

        # Encabezado
        #story.append(Paragraph("<b>ACCECORT</b>", styles["Title"]))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"<b>Cliente:</b> {self.client['name']}", styles["Normal"]))
        if self.client['adress']:
            story.append(Paragraph(f"<b>Direccion:</b> {self.client['adress']}", styles["Normal"]))
        if self.client['phone']:
            story.append(Paragraph(f"<b>Telefono:</b> {self.client['phone']}", styles["Normal"]))
        story.append(Paragraph(f"<b>Fecha:</b> {self.ticket['date']}", styles["Normal"]))
        story.append(Spacer(1, 12))

        # Tabla de productos
        data = [["Producto", "Cantidad", "Precio Unitario", "Subtotal"]]
        for item in self.ticket["items"]:
            data.append([
                item["name"],
                str(item["amount"]),
                f"${item['unit_price']:.2f}",
                f"${item['subtotal']:.2f}"
            ])

        table = Table(data, colWidths=[90*mm, 30*mm, 35*mm, 35*mm])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
            ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
            ("ALIGN", (1,1), (-1,-1), "CENTER"),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
        ]))
        story.append(table)
        story.append(Spacer(1, 15))

        # Totales
        story.append(Paragraph(f"<b>Subtotal:</b> ${self.ticket['subtotal']:.2f}", styles["Normal"]))
        story.append(Paragraph(f"<b>Descuento:</b> {self.ticket['discount']}%", styles["Normal"]))
        story.append(Paragraph(f"<b>Total:</b> ${self.ticket['total']:.2f}", styles["Normal"]))
        story.append(Spacer(1, 20))

        story.append(Paragraph("<i>Emitido por accecort</i>", styles["Normal"]))

        # Construir PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
