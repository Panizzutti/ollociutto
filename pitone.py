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
            | (df['countriesAndTerritories'] == 'Turks_and_Caicos_islands')
            | (df['countriesAndTerritories'] == '')
            | (df['countriesAndTerritories'] == '')
            | (df['countriesAndTerritories'] == '')
            ),:]

df = df.reset_index(drop= True )

date = df['dateRep'].drop_duplicates()
date = pd.to_datetime(date).sort_values().to_frame().rename(columns={"dateRep": "DATE"})

listadate = date["DATE"]

date = date.set_index("DATE")
date.index.name = "DATE"

countries = df['countriesAndTerritories'].drop_duplicates()

date = pd.concat([date,pd.DataFrame(columns=countries)])

date.to_csv('date.csv', index=True)

casi = date.copy(deep=True)
morti = date.copy(deep=True)

for n in range( df.shape[0]  ):
    linea = df.iloc[n]

    casi.at[ linea.dateRep, linea.countriesAndTerritories] = linea.cases
    morti.at[ linea.dateRep, linea.countriesAndTerritories] = linea.deaths



casi.to_csv('casi.csv', index=True)
morti.to_csv('morti.csv', index=False)






