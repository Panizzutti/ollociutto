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

date = date.set_index('DATE')
date.index.name = "DATE"

countries = df['countriesAndTerritories'].drop_duplicates()

popolazioni= countries.copy(deep=True).to_frame()
popolazioni = popolazioni.set_index('countriesAndTerritories')
popolazioni["abitanti"] = ""


date = pd.concat([date,pd.DataFrame(columns=countries)])


casi = date.copy(deep=True)
morti = date.copy(deep=True)

casim = casi.copy(deep=True)
mortim = morti.copy(deep=True)

for n in range( df.shape[0]  ):
    linea = df.iloc[n]

    casi.at[ linea.dateRep, linea.countriesAndTerritories] = linea.cases
    morti.at[ linea.dateRep, linea.countriesAndTerritories] = linea.deaths
    casim.at[ linea.dateRep, linea.countriesAndTerritories] = (linea.cases)/(linea.popData2018)*1000000
    mortim.at[ linea.dateRep, linea.countriesAndTerritories] = (linea.deaths)/(linea.popData2018)*1000000
 
    popolazioni.at[linea.countriesAndTerritories, "abitanti"] = linea.popData2018


casi = casi.fillna(0)
morti = morti.fillna(0)
casim = casim.fillna(0)
mortim = mortim.fillna(0)

casimed = casim.copy(deep=True)
mortimed = mortim.copy(deep=True)


casimed = casim.rolling(window = 6, min_periods=1).mean().round(1)
mortimed = mortim.rolling(window = 6, min_periods=1 ).mean().round(1)


casimed.to_csv('grapheu.csv', index=True, index_label="DATE", date_format="%d/%m/%Y")
mortimed.to_csv('graphdeu.csv', index=True, index_label="DATE", date_format="%d/%m/%Y")
casimed.to_csv('graphus.csv', index=True, index_label="DATE", date_format="%m/%d/%Y")
mortimed.to_csv('graphdus.csv', index=True, index_label="DATE", date_format="%m/%d/%Y")

