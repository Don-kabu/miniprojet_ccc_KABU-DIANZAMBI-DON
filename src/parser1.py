
import json
import re
import docx2txt
import pandas as pd

def get_docx_text(docx_path):
    data = docx2txt.process(docx_path)
    return data

def get_page_number(text):
    pagepattern = r'\d+/\d+\n'
    match = re.findall(pagepattern, text)
    if match:
        return match[0].split('/')[1].strip()
    return None


def get_meta_data(text):
    metadata = {}
    sampleid_pattern = r'[A-Z0-9]+-\d{4}-[A-Z0-9]+-\d+'
    operator_pattern = r'[A-Z0-9]+/[A-Z0-9]+, \d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}'
    time_pattern = r'\d{2}:\d{2}:\d{2}'
    date_pattern = r'\d{2}/\d{2}/\d{4}'
    
    sampleid_match = re.search(sampleid_pattern, text)
    operator_match = re.search(operator_pattern, text)
    time_match = re.search(time_pattern, text)
    date_match = re.search(date_pattern, text)
    
    if sampleid_match:
        metadata['SampleID'] = sampleid_match.group(0)
    if operator_match:
        metadata['Operator'] = operator_match.group(0)
    if time_match:
        metadata['Time'] = time_match.group(0)
    if date_match:
        metadata['Date'] = date_match.group(0)
    
    return metadata





def get_author_info(text):
    author_pattern = r"©\s\d{4}\s*[A-za-z]+\s*[A-za-z]*\s*[A-za-z]*\s*"
    match = re.findall(author_pattern, text)
    data = {
        "author": re.search(r'[A-za-z]+\s*[A-za-z]*\s*[A-za-z]*', match[0]).group(0) if match else "",
        "year": re.search(r'\d{4}', match[0]).group(0) if match else ""
    }
    if match:
        return data
    return None

def get_conclusion(text):
    conclusion_pattern = r'Conclusion\s:\s([a-zA-Z0-9]*)'
    match = re.findall(conclusion_pattern, text)
    data = []
    if match:
        return [match[i].split(':')[-1].strip() for i in range(len(match))]
    return None






# import re
def extract_test_parameters(text):

    sections = re.split(r"Name test:\s*", text, flags=re.IGNORECASE)
    sections = [s.strip() for s in sections if s.strip()]

    result = {}
    block_pattern = re.compile(
        r"name\s*(?P<name>.+?)\s*"
        r"filename\s*(?P<filename>.+?)\s*"
        r"step\s*(?P<step>.+?)\s*"
        r"pre-amplifier\s*(?P<preamp>.+?)\s*"
        r"set up\s*(?P<setup>.+?)\s*"
        r"number of sweeping\s*(?P<sweeping>.+?)\s*"
        r"RBW\s*(?P<rbw>.+?)\s*"
        r"dynamic\s*(?P<dynamic>.+?)\s*"
        r"Span\s*(?P<span>.+?)\s*"
        r"reference level\s*(?P<ref_level>.+?)\s*"
        r"VBW\s*(?P<vbw>.+?)\s*"
        r"RF attenuation\s*(?P<rf_att>.+?)\s*"
        r"sweep time\s*(?P<sweep_time>.+?)\s*"
        r"RF attenuation min\s*"
        r"Maxhold\s*(?P<maxhold>.+?)\s*",
        re.DOTALL | re.IGNORECASE
    )

    for section in sections:
        # La première ligne est le test_name
        lines = section.splitlines()
        test_name = lines[0].strip()
        body = "\n".join(lines[1:])

        result[test_name] = {}
        for i, match in enumerate(block_pattern.finditer(body), start=1):
            result[test_name][i] = {k: (v.strip() if v else None) for k, v in match.groupdict().items()}

    return result









data = extract_test_parameters(get_docx_text("input/RAW DATA 02.doc"))
print(set(data))