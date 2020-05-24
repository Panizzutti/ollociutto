import numpy as np
import pandas as pd

from pandas import ExcelFile


df = pd.read_excel('covid.xlsx')

df = df.loc[~((df['countriesAndTerritories'] == 'Anguilla') 
            | (df['countriesAndTerritories'] == 'Falkland_Islands_(Malvinas)')
            | (df['countriesAndTerritories'] == 'Eritrea')
            | (df['countriesAndTerritories'] == 'Bonaire, Saint Eustatius and Saba')
            | (df['countriesAndTerritories'] == 'Western_Sahara')
            | (df['countriesAndTerritories'] == 'Cases_on_an_international_conveyance_Japan')
            | (df['countriesAndTerritories'] == 'CuraÃ§ao')
            | (df['countriesAndTerritories'] == '')
            | (df['countriesAndTerritories'] == '')
            | (df['countriesAndTerritories'] == '')
            ),:]

date = df['dateRep'].drop_duplicates()
date = pd.to_datetime(date)
date = date.sort_values().to_frame()
date =date.reset_index(drop=True)
date.rename(columns={"dateRep": "DATE"})
print(date)
date.to_csv('date.csv',index=False,)