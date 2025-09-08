
##################################################################################
##################################################################################
#######                     settings.py                                 ##########
#######                    ______________                               ##########
#######    this file contains settings for the project including        ##########
#######    files path configurations, default  values ,regex patterns,  ##########
#######    reusable values and other essential settings.                ##########
#######                                                                 ##########
##################################################################################
##################################################################################
import os 
import re





INPUTFILE = "input/RAW DATA 02.doc"


ROOT = os.getcwd()
DATA_DIR = os.path.join(ROOT, 'data')
INPUT_DIR = os.path.join(DATA_DIR, 'input')
OUTPUT_DIR = os.path.join(ROOT, 'output')
TEMPLATE_DIR = os.path.join(DATA_DIR, 'templates')  
LOG_FILE  =  os.path.join(ROOT,"out/.log")








BLOCK_PATTERN = pattern = re.compile(
        r"(EQ/MR\s+\d+:\s+Measurement of radio frequency radiated emission test.*?)"
        r"(?=(?:EQ/MR\s+\d+:)|\Z)",  # s'arrête au prochain EQ/MR ou fin du texte
        re.DOTALL
    )



MESURE_TITLES = [
        "CISPR.AVG/Lim.Avg (2)",
        "Peak/Lim.Q-Peak (2)",
        "Q-Peak/Lim.Q-Peak (2)",
        "Peak/Lim.Peak (2)"
    ]
    


MESURE_DATA_PATTERN = re.compile(
        r"(?P<title>" + "|".join(map(re.escape, MESURE_TITLES)) + r")\s+"
        r"(?P<body>.*?(?:Vertical|Horizontal)\s+\d+\.\d+\s+.*?(?:Vertical|Horizontal)\s+\d+\.\d+)",
        re.DOTALL
    )



TEST_PARAMETERS_BLOCK_PATTERN = block_pattern = re.compile(
        r"\s*\n\n\n\s*"
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



META_DATA_PATTERN = re.compile(
        r"Sample:\s*(?P<sample>.*?)\s*"
        r"Project:\s*(?P<project>.*?)\s*"
        r"Operator:\s*(?P<operator>.*?)\s*"
        r"Test Configuration:\s*(?P<test_config>.*?)\s*"
        r"Operating mode:\s*(?P<operating_mode>.*?)(?=\n\n|\Z)",
        re.DOTALL
    )


candidate = "KABU DIANZAMBI DON"