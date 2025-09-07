##################################################################################
##################################################################################
#######                     main.py                                     ##########
#######                    ______________                               ##########
#######    this file is the root file of the project and        
#######    contains the root or main logic of the project               ##########
#######                                                                 ##########
##################################################################################
##################################################################################

from docx import Document
from utils import save_log
# from ..config import settings







# writting to log
save_log()



doc = Document()
doc.add_heading('Main Document', 0)
doc.add_paragraph('This is the main logic of the project.')
doc.save('main_document.docx')
