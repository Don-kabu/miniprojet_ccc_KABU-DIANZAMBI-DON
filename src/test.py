import docx2txt
import utils as utl
import json
import pandas as pd

text = docx2txt.process("input/RAW DATA 02.doc").replace("Â","")


data = utl.getdata(text)
data =utl.get_cleaned_data(data)










print("Export CSV et Excel terminés avec succès!")
print(f"Nombre d'enregistrements traités: {len(df)}")