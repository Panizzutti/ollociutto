import numpy as np
import pandas as pd

from pandas import ExcelFile

df = pd.read_excel('covid.xlsx')

c= df['dateRep'].drop_duplicates()

print(c)

df.to_csv()
