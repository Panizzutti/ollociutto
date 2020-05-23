import numpy as np
import pandas as pd

from pandas import ExcelFile

df = pd.read_excel('covid.xlsx')
a = df['dateRep'].unique()

b = a['dateRep'].dt.strftime('%m/%d/%Y')

print(sorted(a))