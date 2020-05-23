
import numpy as np
import pandas as pd

from pandas import ExcelFile


df = pd.read_excel('covid.xlsx') # read xlsx diretto da eu
df.fillna(0)
pd.set_option("display.precision", 3)

# Don't wrap repr(DataFrame) across additional lines
pd.set_option("display.expand_frame_repr", False)

# Set max rows displayed in output to 25
pd.set_option("display.max_rows", 25)
""" print(df.head(100)) """
""" df["casesM"] = 
 """
df["test"] = df["cases"].rolling(window=5,min_periods=1).mean()
#print("Column headings:")
#print(df.head(100))
#print(df.columns,df.values)
df.fillna(0)
df = df.replace(np.nan, 0)
print(df.describe())
df1=df[:5]
df1.plot("dateRep","test",kind = 'line')


df.to_csv("test.csv")
    