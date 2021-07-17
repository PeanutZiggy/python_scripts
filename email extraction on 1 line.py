import pandas as pd

df = pd.read_excel("emails.xlsx")
print(df)
for i in df['Names']:
    print(i, ';', end=" ")