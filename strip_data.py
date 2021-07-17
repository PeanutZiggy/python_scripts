import pandas as pd

df = pd.read_excel("USR_COMP.xlsx")
df['User_ad_acct'] = df['User_ad_acct'].astype(str)

for i in df.index:

    val = df.loc[i, 'User_ad_acct']

    if '(' not in val:
        continue

    else:
        openbr = val.find('(')
        val = val[openbr:]
        val = val.replace('(', '')
        val = val.replace(')', '')

    print(val)
    df.loc[i,'User_ad_acct'] = val

df.to_excel (r'C:\Users\KitovYo\Downloads\TEST.xlsx')
