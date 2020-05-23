import numpy as np
import pandas as pd

from pandas import ExcelFile

df = pd.read_excel('covid.xlsx')
df = df.dropna() #rimozione anguilla e merde
date = df['dateRep'].drop_duplicates()
print(date)
df.to_csv()
