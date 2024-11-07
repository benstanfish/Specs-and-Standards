import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import os
from pathlib import Path

from tkinter import Tk
from tkinter import filedialog

Tk().withdraw()
file_name = filedialog.askopenfilename()
csv_name = os.path.dirname(file_name) + '\\' + Path(file_name).stem + '.csv'

if Path(file_name).suffix.lower() == '.sec' or Path(file_name).suffix.lower() == '.ref':
    
    tree = ET.parse(file_name)

    section_number = tree.find('SCN').text[8:]
    section_title = tree.find('STL').text
    section_version = tree.find('DTE').text

    standard_references = tree.findall('*//RID')
    standard_titles = tree.findall('*//RTL')
    standard_count = len(standard_titles)       # Assumes well-formed references: listed in Reference Section

    order = []

    section = []
    section_name = []
    section_ver = []

    refs = []
    editions = []
    titles = []

    for i in range(standard_count):
        order.append(i + 1) 
        
        section.append(section_number)
        section_name.append(section_title)
        section_ver.append(section_version)
        
        refs.append(standard_references[i].text)
        
        standard_title = standard_titles[i].text
        position = standard_title.find(')') + 1
        
        editions.append(standard_title[:position].replace(r'(','').replace(r')',''))
        titles.append(standard_titles[i].text[position+1:])

    column_names = ['Order', 'Section', 'Name', 'Version', 'Standard', 'Edition', 'Title']

    df = pd.DataFrame(list(zip(order, 
                            section, 
                            section_name, 
                            section_ver, 
                            refs, 
                            editions, 
                            titles)), 
                    columns=column_names)                  # Zip the two lists together and convert to dataframe

    df.to_csv(csv_name, index=False)