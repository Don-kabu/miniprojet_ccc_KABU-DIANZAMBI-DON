from docx import Document
import docx2txt
from writter import create_document
import utils
import json
from config import INPUTFILE,OUTPUT_DIR
import os
# from ..config import settings


file_path = INPUTFILE


rawtext = docx2txt.process(file_path).replace("Â","")

data = utils.getdata(rawtext)

# importantdata = extract_important_data(data)
importantdata = utils.get_cleaned_data(data)

filename = utils.get_filename_from_path(file_path)

# try:

if not os.path.exists(OUTPUT_DIR+f"/{filename}"):
    os.mkdir(OUTPUT_DIR+f"/{filename}/")

with open(OUTPUT_DIR+f"/{filename}/genarated.json","w") as file : 
    json.dump(importantdata,file,indent=4,ensure_ascii=False)

with open(OUTPUT_DIR+f"/{filename}/full.json","w",encoding="utf-8") as file:
    json.dump(data,file,indent=4,ensure_ascii=False)
    
# Traiter les données
df = utils.getdataframe(importantdata)

# Exporter en CSV
df.to_csv(OUTPUT_DIR+f"/{filename}"+'/POCESSED.csv', index=False, encoding='utf-8')

# Exporter en Excel
df.to_excel(OUTPUT_DIR+f"/{filename}"+'/POCESSED.xlsx', index=False, engine='openpyxl')

print(f"""
    file exported succesfully
    =========================
    csv : out_{filename}.csv
    excel : out_{filename}.excel
    docx : processed_{filename}.docx
    full extracted data : {filename}_FULL.json
    important used data  : {filename}_IMPORTANT.json
    """)

# except :
#     print("""
#         SOME THING WENT WRONG  CHECK YOUR FILE PATH 
#     """)
#     data = None
