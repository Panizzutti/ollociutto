import numpy as np
import pandas as pd
import os

from pandas import ExcelFile

#remove \n to last line 
def toglilinea(filename):
    with open(filename, 'rb+') as f:
        f.seek(-1, os.SEEK_END)
        if(f.readline() == b'\n'):
                f.seek(-1, os.SEEK_END)
                f.truncate()

df = pd.read_excel('covid.xlsx')

#remove unwanted countries
df = df.loc[~((df['countriesAndTerritories'] == 'Anguilla') 
            | (df['countriesAndTerritories'] == 'Falkland_Islands_(Malvinas)')
            | (df['countriesAndTerritories'] == 'Eritrea')
            | (df['countriesAndTerritories'] == 'Bonaire, Saint Eustatius and Saba')
            | (df['countriesAndTerritories'] == 'Western_Sahara')
            | (df['countriesAndTerritories'] == 'Cases_on_an_international_conveyance_Japan')
            | (df['countriesAndTerritories'] == 'CuraÃ§ao')
            | (df['countriesAndTerritories'] == 'Turks_and_Caicos_islands')
            | (df['countriesAndTerritories'] == 'Turks_and_Caicos_islands')
            | (df['countriesAndTerritories'] == 'British_Virgin_Islands')
            | (df['countriesAndTerritories'] == 'Saint_Kitts_and_Nevis')
            | (df['countriesAndTerritories'] == '')
            | (df['countriesAndTerritories'] == '')
            | (df['countriesAndTerritories'] == '')
            | (df['countriesAndTerritories'] == '')
            | (df['countriesAndTerritories'] == '')
            ),:]

df = df.reset_index(drop= True )

#create an ordered list of all dates
date = df['dateRep'].drop_duplicates()
date = pd.to_datetime(date).sort_values().to_frame().rename(columns={"dateRep": "DATE"})

#save for later the list of dates
listadate = date["DATE"]

#put dates as index
date = date.set_index('DATE')

#create a list of the wanted countries
countries = df['countriesAndTerritories'].drop_duplicates()

#create a df of the populations
popolazioni= countries.copy(deep=True).to_frame()
popolazioni = popolazioni.set_index('countriesAndTerritories')
popolazioni["abitanti"] = ""

#pre format the dataframe to host the datas
date = pd.concat([date,pd.DataFrame(columns=countries)])


casi = date.copy(deep=True)
morti = date.copy(deep=True)

casim = casi.copy(deep=True)
mortim = morti.copy(deep=True)

#analise the whole xlsx file, line by line and fill graphs
for n in range( df.shape[0]  ):
    linea = df.iloc[n] #get the nth line 

    #put values from linea in right place
    casi.at[ linea.dateRep, linea.countriesAndTerritories] = linea.cases
    morti.at[ linea.dateRep, linea.countriesAndTerritories] = linea.deaths
    casim.at[ linea.dateRep, linea.countriesAndTerritories] = (linea.cases)/(linea.popData2018)*1000000
    mortim.at[ linea.dateRep, linea.countriesAndTerritories] = (linea.deaths)/(linea.popData2018)*1000000
    #put population values
    popolazioni.at[linea.countriesAndTerritories, "abitanti"] = linea.popData2018

#fill empty cells with 0s
casi = casi.fillna(0)
morti = morti.fillna(0)
casim = casim.fillna(0)
mortim = mortim.fillna(0)

casimed = casim.copy(deep=True)
mortimed = mortim.copy(deep=True)

#moving average of casim e mortim
casimed = casim.rolling(window = 6, min_periods=1).mean().round(1)
mortimed = mortim.rolling(window = 6, min_periods=1 ).mean().round(1)

#create csv files
casimed.to_csv('grapheu.csv', index=True, index_label="DATE", date_format="%d/%m/%Y")
mortimed.to_csv('graphdeu.csv', index=True, index_label="DATE", date_format="%d/%m/%Y")
casimed.to_csv('graphus.csv', index=True, index_label="DATE", date_format="%m/%d/%Y")
mortimed.to_csv('graphdus.csv', index=True, index_label="DATE", date_format="%m/%d/%Y")

#remove extra line that pandas creates in conversion to csv
toglilinea("grapheu.csv")
toglilinea("graphdeu.csv")
toglilinea("graphus.csv")
toglilinea("graphdus.csv")


