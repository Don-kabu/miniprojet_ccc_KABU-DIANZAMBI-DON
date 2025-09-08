from importlib import metadata
from docx import Document
from docx.shared import Pt, Inches,RGBColor
from datetime import datetime
import pandas as pd 
from config import candidate
import json
from docx.oxml import OxmlElement
from docx.oxml.ns import qn




def add_footer(doc, left_text, center_text = datetime.strftime(datetime.now(),"%d/%m/%Y, %H:%M:%S"), right_text=""):
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





def generate_csv_output(json_data:dict, output_path):
    # Préparation des données pour CSV
    csv_data = []
    for config in json_data:
        for measurement in config['measurements']:
            row = {
                'Sample': config['metadata']['sample'],
                # 'Configuration': config["parameters"]['name'],
                'RBW': config['parameters']['rbw'],
                'Frequency': measurement['frequency'],
                'Measurement': measurement['measurement'],
                'Limit': measurement['limit'],
                'Margin': measurement['margin'],
                'Verdict': measurement['verdict']
            }
            csv_data.append(row)
    
    # Écriture CSV
    df = pd.DataFrame(csv_data)
    df.to_csv(output_path, index=False)















# Fonction pour ajouter un style de tableau professionnel
def style_table(table):
    # Bordures fines
    tbl = table._element
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ("top", "left", "bottom", "right", "insideH", "insideV"):
        border = OxmlElement(f"w:{border_name}")
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '8')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), '2F5496')  # bleu foncé
        tblBorders.append(border)
    tbl.tblPr.append(tblBorders)










def add_measurements_table(doc, measurements, title="Tableau des mesures"):
    """
    Ajoute un tableau de mesures dans le document Word
    :param doc: objet Document (python-docx)
    :param measurements: liste de dicts (test_data["measurements"])
    :param title: titre de la section
    """

    if not measurements:
        doc.add_heading(title, level=2)
        doc.add_paragraph()
        doc.add_paragraph("PAS DE MESURE POUR CETTE SECTION")
        doc.add_paragraph()
        return

    # Ajouter un titre
    doc.add_heading(title, level=2)

    # Définir les colonnes à afficher
    colonnes = [
        "measurement_type", "frequency_mhz", "Limit", "Margin",
        "polarization", "correction_db", "Measured", "veridict"
    ]

    # Créer le tableau
    table = doc.add_table(rows=1, cols=len(colonnes))
    table.style = "Light List Accent 3"

    # En-têtes
    hdr_cells = table.rows[0].cells
    for i, col in enumerate(colonnes):
        hdr_cells[i].text = col.replace("_", " ").capitalize()

    # Remplir le tableau
    for measure in measurements:
        row_cells = table.add_row().cells
        for i, col in enumerate(colonnes):
            text_value = str(measure.get(col, ""))

            # Ajouter du texte coloré dans la cellule
            p = row_cells[i].paragraphs[0]
            run = p.add_run(text_value)

            if text_value.lower() == "fail":
                run.font.color.rgb = RGBColor(255, 0, 0)  # Rouge
            elif text_value.lower() == "pass":
                run.font.color.rgb = RGBColor(0, 128, 0)  # Vert
            else:
                run.font.color.rgb = RGBColor(0, 0, 0)  # Noir par défaut

    # Appliquer un style de bordures
    tbl = table._element
    tblBorders = OxmlElement("w:tblBorders")
    for border_name in ("top", "left", "bottom", "right", "insideH", "insideV"):
        border = OxmlElement(f"w:{border_name}")
        border.set(qn("w:val"), "single")
        border.set(qn("w:sz"), "6")
        border.set(qn("w:space"), "0")
        border.set(qn("w:color"), "C00000")  # Rouge sombre
        tblBorders.append(border)
    tbl.tblPr.append(tblBorders)

    doc.add_paragraph()











def create_document(data,out_filename):
    # Créer document Word
    doc = Document()

    # Titre principal
    title = doc.add_heading("Rapport  de Test", level=0)
    title.alignment = 1  # centré

    # Boucler sur chaque test
    for test_name, test_data in data.items():
        doc.add_heading(f"🔹 {test_name}", level=1)

        # Infos générales
        doc.add_heading("Informations générales", level=2)
        info_table = doc.add_table(rows=1, cols=2)
        info_table.style = "Light List Accent 1"
        hdr_cells = info_table.rows[0].cells
        hdr_cells[0].text, hdr_cells[1].text = "Clé", "Valeur"

        for key in ["sample_id", "antenna_position", "mode", "dut_orientation"]:
            row_cells = info_table.add_row().cells
            row_cells[0].text = key.replace("_", " ").capitalize()
            row_cells[1].text = str(test_data.get(key, ""))

        style_table(info_table)
        doc.add_paragraph()

        # Paramètres de test
        doc.add_heading("Paramètres de test", level=2)
        params = test_data.get("parameters", {})
        param_table = doc.add_table(rows=1, cols=2)
        param_table.style = "Light List Accent 2"
        hdr_cells = param_table.rows[0].cells
        hdr_cells[0].text, hdr_cells[1].text = "Paramètre", "Valeur"

        for k, v in params.items():
            row_cells = param_table.add_row().cells
            row_cells[0].text = k
            row_cells[1].text = str(v)

        style_table(param_table)
        doc.add_paragraph()
        add_measurements_table(doc,test_data["measurements"])
        

    add_footer(doc,candidate,right_text=out_filename)

    # Sauvegarder document
    doc.save(f"out/Processed_{out_filename}.docx")
 


