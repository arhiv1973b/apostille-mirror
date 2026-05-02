from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
font_path = os.path.join(os.environ['WINDIR'], 'Fonts', 'arial.ttf')
pdfmetrics.registerFont(TTFont('Arial', font_path))
c = canvas.Canvas("identity-certificate.pdf", pagesize=A4)
w, h = A4
c.setFont("Arial", 16); c.drawCentredString(w/2, h - 100, "IDENTITY VERIFICATION CERTIFICATE")
c.setFont("Arial", 12); c.drawString(100, h - 200, "Legal Subject: Maceret Alexei")
c.drawString(100, h - 220, "Digital Identity: A©tor")
c.drawString(100, h - 240, "IDNP: 2000001159655")
c.drawString(100, h - 260, "Case ID: CASE-MACHERET-1997-2026")
c.setFont("Arial", 8); c.drawString(100, 100, "GPG Signed: 7BEACB5463BA3007")
c.save()
