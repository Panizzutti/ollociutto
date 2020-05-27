import numpy as np
import pandas as pd
import os

from pandas import ExcelFile



#sum each colum
""" def totale(df, riga):
    for column in df:
        informazioni.at[riga, column]= df[column].sum() """
""" def totale(df, riga):
    informazioni.loc[riga]= df.sum() """

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
datess = df['dateRep'].drop_duplicates()
datess = pd.to_datetime(datess).sort_values(ascending=False)#.to_frame().rename(columns={"dateRep": "DATE"})


for z in datess:

    date = df['dateRep'].drop_duplicates()
    date = pd.to_datetime(date).sort_values().to_frame().rename(columns={"dateRep": "DATE"})



    #save for later the list of dates
    listadate = date["DATE"]

    #put dates as index
    date = date.set_index('DATE')

    #create a list of the wanted countries
    countries = df['countriesAndTerritories'].drop_duplicates().reset_index(drop=True)


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
    informazioni["tendenzacasi"] = ""
    informazioni["tendenzamorti"] = ""
    #informazioni[""] = ""

    informazioni= informazioni.transpose()

    #get the rank
    def rankinator(riga, ascending, pct):
        informazioni.loc['rank' + riga] = informazioni.loc[riga].rank(method='dense', ascending=ascending, pct=pct)

    #calculate a ponderate score for each country
    def punteggio(argomento):
        somma=[]
        for column in informazioni.columns:
            somma.append(informazioni.at[ "rank"+argomento+"med" ,column] + 
                        informazioni.at[ "rank"+argomento+"med" ,column] + 
                        informazioni.at[ "rank"+argomento+"med" ,column] + 
                        informazioni.at[ "rank"+argomento+"tot" ,column] + 
                        informazioni.at[ "rank"+argomento+"tot" ,column] +
                        informazioni.at[ "rankpopolazione" ,column] )
        informazioni.loc["punteggio"+argomento]=somma


    #calculate trend
    def tendenzieitor(argomento, inforiga):
        tendenze = [] 
        for i in range(argomento.shape[1]):
            valoriora = float((argomento.iat[-1, i] +
                            argomento.iat[-2, i])/2 )
            valoriprima = float((argomento.iat[-3, i] +
                            argomento.iat[-4, i])/2)
            valdiff = valoriora - valoriprima
            confidence = (((valoriora + valoriprima)/2)*0.02)

            if(valdiff< -confidence):
                tendenze.append(0)
            elif(valdiff> confidence):
                tendenze.append(2)
            else:
                tendenze.append(1)

        informazioni.loc["tendenza"+inforiga]= tendenze


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
    informazioni.loc["casitot"]= casi.sum()
    informazioni.loc["mortitot"]= morti.sum()

    casimed = casim.copy(deep=True)
    mortimed = mortim.copy(deep=True)

    #moving average of casim e mortim
    casimed = casim.rolling(window = 6, min_periods=1).mean().round(1)
    mortimed = mortim.rolling(window = 6, min_periods=1 ).mean().round(1)


    #remove extra line that pandas creates in conversion to csv

    informazioni.loc["casimed"] = casimed.iloc[-1]
    informazioni.loc["mortimed"] = mortimed.iloc[-1]


    #get the rank of each category in each country
    rankinator("casitot", False, True)
    rankinator("mortitot", False, True)
    rankinator("popolazione", False, True)
    rankinator("casimed", False, True)
    rankinator("mortimed", False, True)

    #get countries deaths and cases scores
    punteggio("casi")
    punteggio("morti")

    #get final ranks
    rankinator("punteggiocasi", True, False)
    rankinator("punteggiomorti", True, False)

    tendenzieitor(casimed, "casi")
    tendenzieitor(mortimed, "morti")

    casiglobalitotali= casi.sum()
    mortiglobalitotali= morti.sum()



    casifinale= pd.DataFrame()
    mortifinale= pd.DataFrame()


    casifinale= pd.concat([informazioni.loc["rankpunteggiocasi"],
                        informazioni.columns.to_series(),
                        informazioni.loc["casimed"],
                        informazioni.loc["tendenzacasi"],
                        casi.iloc[-1],
                        informazioni.loc["casitot"]
                        ], axis=1) 


    mortifinale= pd.concat([informazioni.loc["rankpunteggiomorti"],
                        informazioni.columns.to_series(),
                        informazioni.loc["mortimed"],
                        informazioni.loc["tendenzamorti"],
                        morti.iloc[-1],
                        informazioni.loc["mortitot"]
                        ], axis=1) 



    casifinale.columns = ['Rank', 'Country',	'CaseM',	'Tendenza',	'CaseNew',	'Casitot']
    mortifinale.columns = ['Rank', 'Country',	'CaseM',	'Tendenza',	'CaseNew',	'Casitot']

    casifinale= casifinale.sort_values('Rank')
    mortifinale= mortifinale.sort_values('Rank')

    casifinale.to_csv("storico/rank-"+str(z.date())+".csv", index=False)

    mortifinale.to_csv("storico/rankd-"+str(z.date())+".csv", index=False)
    df = df.loc[~((df['dateRep'] == z)),:]


