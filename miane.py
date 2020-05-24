import numpy as np
import pandas as pd

from pandas import ExcelFile

df = pd.read_excel('covid.xlsx')
df = df.dropna() #rimozione anguilla e merde
df = df.reset_index(drop=True)
date= df['dateRep'].drop_duplicates()
rank = date.to_frame() #dataframe con le date univoche per il rank
print(rank)