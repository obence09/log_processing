#Csoportosított havi min és max átlaghőmérséklet

import os
from pathlib import Path
import pandas as pd
import pyinputplus
import numpy

#Inputot bekérni
import_path = pyinputplus.inputFilepath('Please enter the import filepath: \n')
mypath = Path(import_path)

export_path = pyinputplus.inputFilepath('Please enter the export filepath: \n')
outputpath = Path(export_path)

ouput_filname = pyinputplus.inputStr('Please enter the name of the output file: \n') + '.csv'

#Listákat létrehozni a beolvasott részegységeknek, lista a fileoknak
chunk_list = []
file_list = sorted(os.listdir(mypath), reverse=True)

#1, Beolvasni az összes file-t részletekben
for filename in file_list:
    chunk_list = pd.read_csv(mypath/filename,usecols=[1,2,3],
                sep= ',',
                names=['month','min-max','value'],
                dtype={'month':str, 'min-max':str, 'value':numpy.int16},
                chunksize=1000000,
                engine='c')

datafr = pd.DataFrame(pd.concat(chunk_list))
datafr['month'] = datafr['month'].str[4:6]
datafr = datafr[(datafr['min-max'] == 'TMAX') | (datafr['min-max'] == 'TMIN')]

#2, hónapokra group-olva átlagolni az értékeket 12 x 1-min és 1-max érték
month_grouped = datafr.groupby(['month','min-max']).mean().reset_index()

#3, az eredményt kiexportálni egy csv-be
month_grouped.to_csv(outputpath / ouput_filname ,header=['month','min-max','temperature'])
