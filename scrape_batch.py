import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import os, datetime
from pathlib import Path

from tkinter import Tk
from tkinter import filedialog

Tk().withdraw()
folder_name = filedialog.askdirectory()
csv_name = folder_name + '\\Reference Standards Report ' + '{:%Y%m%d %H%M%S}'.format(datetime.datetime.now()) + '.csv'

list_of_dfs = []

for file_name in os.listdir(folder_name):

    try:                                        # Skip files that contain parsing errors or NO references
        if (Path(file_name).suffix.lower() == '.sec'):  # and (Path(file_name).stem[:2] != '01'):   #<-- this adds the condition of ignoring Div 01
            
            tree = ET.parse(folder_name + '\\' + file_name)

            section_number = tree.find('SCN').text[8:]
            section_title = tree.find('STL').text
            section_version = tree.find('DTE').text

            standard_references = tree.findall('*//RID')
            standard_titles = tree.findall('*//RTL')
            standard_count = len(standard_titles)       # Assumes well-formed references: listed in Reference Section

            section = []
            section_name = []
            section_ver = []

            refs = []
            editions = []
            titles = []

            for i in range(standard_count):

                section.append(section_number)
                section_name.append(section_title)
                section_ver.append(section_version)

                refs.append(standard_references[i].text)

                standard_title = standard_titles[i].text
                position = standard_title.find(')') + 1

                editions.append(standard_title[:position].replace(r'(','').replace(r')',''))
                titles.append(standard_titles[i].text[position+1:])

            df = pd.DataFrame(list(zip(section,
                                    section_name,
                                    section_ver,
                                    refs,
                                    editions,
                                    titles)))           # Zip the two lists together and convert to dataframe

            list_of_dfs.append(df)
    except:
        pass
    
with open(csv_name, 'a') as f:
    for df in list_of_dfs:
        df.to_csv(f, index=True, header=False, lineterminator='\n')