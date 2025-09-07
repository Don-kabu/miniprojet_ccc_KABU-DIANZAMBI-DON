from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

def add_footer(doc, left_text, center_text, right_text):
    section = doc.sections[0]
    footer = section.footer

    # Supprimer anciens paragraphes si besoin
    for p in footer.paragraphs:
        p.clear()

    # Créer un tableau 1x3
    table = footer.add_table(rows=1, cols=3, width=Inches(8.0))
    table.autofit = False  

    # Fixer les largeurs manuellement
    widths = [Inches(2.5), Inches(2.5), Inches(2.5)]
    for cell, width in zip(table.rows[0].cells, widths):
        cell.width = width

    cells = table.rows[0].cells

    # Texte gauche
    left_paragraph = cells[0].paragraphs[0]
    left_run = left_paragraph.add_run(left_text)
    left_run.font.size = Pt(10)

    # Texte centre
    center_paragraph = cells[1].paragraphs[0]
    center_run = center_paragraph.add_run(center_text)
    center_run.font.size = Pt(10)

    # Texte droite
    right_paragraph = cells[2].paragraphs[0]
    right_run = right_paragraph.add_run(right_text)
    right_run.font.size = Pt(10)


if __name__ == "__main__":
    doc = Document()
    doc.add_paragraph("Ceci est un test avec footer aligné.")

    date_now = datetime.now().strftime("%d/%m/%Y")
    add_footer(doc, "KABU DIANZAMBI DON", date_now, "RAW DATA 02")

    doc.save("test_footer.docx")
    print("✅ Document généré avec footer !")
