import numpy as np
import pandas as pd
import os

from pandas import ExcelFile



#sum each colum
def totale(df, riga):
    for column in df:
        informazioni.at[riga, column]= df[column].sum()

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
#            | (df['countriesAndTerritories'] == '')
#            | (df['countriesAndTerritories'] == '')
#            | (df['countriesAndTerritories'] == '')
#            | (df['countriesAndTerritories'] == '')
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

#create a df of countries infos
informazioni= countries.copy(deep=True).to_frame()
informazioni = informazioni.set_index('countriesAndTerritories')
informazioni["popolazione"] = ""
informazioni["casitot"] = ""
informazioni["mortitot"] = ""
informazioni["casimed"] = ""
informazioni["mortimed"] = ""
informazioni["rankpopolazione"] = ""
informazioni["rankcasimed"] = ""
informazioni["rankmortimed"] = ""
informazioni["rankcasitot"] = ""
informazioni["rankmortitot"] = ""
informazioni["punteggiocasi"] = ""
informazioni["punteggiomorti"] = ""
informazioni["rankpunteggiocasi"] = ""
informazioni["rankpunteggiomorti"] = ""
#informazioni[""] = ""

informazioni= informazioni.transpose()

#get the rank
def rankinator(riga):
    informazioni.loc['rank' + riga, : ] = informazioni.loc[riga,:].rank(method='max', ascending=False)



#pre format the dataframe to host the datas
date = pd.concat([date,pd.DataFrame(columns=countries)])

casi = date.copy(deep=True)
morti = date.copy(deep=True)

casim = casi.copy(deep=True)
mortim = morti.copy(deep=True)

#analise the whole xlsx file, line by line and fill graphs
for n in range( df.shape[0]  ):
     #get the nth line 
    linea = df.iloc[n]

    #put values from linea in right place
    casi.at[ linea.dateRep, linea.countriesAndTerritories] = linea.cases
    morti.at[ linea.dateRep, linea.countriesAndTerritories] = linea.deaths
    casim.at[ linea.dateRep, linea.countriesAndTerritories] = (linea.cases)/(linea.popData2018)*1000000
    mortim.at[ linea.dateRep, linea.countriesAndTerritories] = (linea.deaths)/(linea.popData2018)*1000000
    #put population values
    informazioni.at["popolazione", linea.countriesAndTerritories] = linea.popData2018



#fill empty cells with 0s
casi = casi.fillna(0)
morti = morti.fillna(0)
casim = casim.fillna(0)
mortim = mortim.fillna(0)

#sum casitot and casimed
totale(casi, "casitot")
totale(morti, "mortitot")


casimed = casim.copy(deep=True)
mortimed = mortim.copy(deep=True)

#moving average of casim e mortim
casimed = casim.rolling(window = 6, min_periods=1).mean().round(1)
mortimed = mortim.rolling(window = 6, min_periods=1 ).mean().round(1)

#create csv files
casimed.to_csv('graph.csv', index=True, index_label="DATE", date_format="%d/%m/%Y")
mortimed.to_csv('graphd.csv', index=True, index_label="DATE", date_format="%d/%m/%Y")

#remove extra line that pandas creates in conversion to csv
toglilinea("graph.csv")
toglilinea("graphd.csv")

informazioni.loc["casimed",:] = casimed.iloc[-1, :]
informazioni.loc["mortimed",:] = mortimed.iloc[-1, :]

informazioni.loc["punteggiocasi",:] = (sum(
                                       informazioni.loc["rankcasitot", :],
                                       informazioni.loc["rankcasimed", :],
                                       informazioni.loc["rankpopolazione", :])) 



rankinator("casitot")
rankinator("mortitot")
rankinator("popolazione")
rankinator("casimed")
rankinator("mortimed")
#rankinator("punteggiocasi")
#rankinator("punteggiomorti")

informazioni.to_csv('info.csv', index=True)






