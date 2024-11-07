import xml.etree.ElementTree as ET
import pandas as pd
import os
from pathlib import Path

from tkinter import Tk
from tkinter import filedialog

Tk().withdraw()
folder_name = filedialog.askdirectory()

file_path = folder_name + '\\MASTER.REF'
report_path = os.path.dirname(file_path) + '\\' + 'reference_output.xlsx'

tree = ET.parse(file_path)
refs = tree.findall('REF')

orgs = []
standards = []
titles = []


for ref in refs:

    org = ref.find('ORG').text
    standards_raw = ref.findall('RID')
    titles_raw = ref.findall('RTL')

    try:
        for i in range(len(standards_raw)):
            orgs.append(org)
            standards.append(standards_raw[i].text)
            titles.append(titles_raw[i].text)
    except:
        pass

column_names = ['Organization', 'Standard', 'Title']
df = pd.DataFrame(list(zip(orgs, standards, titles)), columns=column_names)                  # Zip the two lists together and convert to dataframe

df.to_excel(report_path)
    