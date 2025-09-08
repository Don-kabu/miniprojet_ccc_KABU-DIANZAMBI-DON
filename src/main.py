from docx import Document
import docx2txt
from Parser import makedata
from writter import create_document
from utils import extract_important_data,export_to_csv,get_filename_from_path
import json
from config import INPUTFILE
# from ..config import settings


file_path = INPUTFILE


rawtext = docx2txt.process(file_path)
data = makedata(rawtext)
importantdata = extract_important_data(data)
filename = get_filename_from_path(file_path)
try:
    with open(f"out/{filename}_IMPORTANT.json","w") as file : 
        json.dump(importantdata,file,indent=4)

    with open(f"out/{filename}_FULL.json","w",encoding="utf-8") as file:
        json.dump(data,file,indent=4,ensure_ascii=False)
    #export to word 
    create_document(importantdata,out_filename=filename)
    # export to csv
    export_to_csv(importantdata,filename)

    print(f"""
        file exported succesfully
        =========================
        csv : out_{filename}.csv
        docx : processed_{filename}.docx
        full extracted data : {filename}_FULL.json
        important used data  : {filename}_IMPORTANT.json
        """)

except :
    print("cannot open the file")
    data = None
