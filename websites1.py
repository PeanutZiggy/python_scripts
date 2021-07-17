import requests
import xlrd
import pandas as pd
import time

websites = xlrd.open_workbook(r'C:\Users\KitovYo\Downloads\ready scripts\sites.xlsx', on_demand = True).sheet_by_name('Sheet1')
links = []
redirects = []
code = ''
dead_link = ''
data = {'Original Link' : [],
        'Redirected Link' : [],
        'Code' : [],
        'Dead Link' : []}
df = pd.DataFrame(data)

for site in range(1,7802):
    weblink = websites.cell(site, 0).value # change 0 to the column that you are using
    link = 'http://' + weblink
    try:
        r = requests.get(link)
    except:
        dead_link = weblink
        continue
    if link.startswith("http://"):
        link = link.replace('http://', '')
    if link.startswith("www."):
        link = link.strip(link[4])
    if link.endswith('/'):
        link = link.strip(link[-1])

    currLink = r.url
    code = r.status_code
    if currLink.startswith("https://") or currLink.startswith("http://"):
        currLink = currLink.replace('https://', '')
        currLink = currLink.replace('http://', '')
    if currLink.startswith("www."):
        currLink = currLink.replace('www.', '')
    if currLink.endswith('/'):
        currLink = currLink.strip(currLink[-1])
    if link != currLink:
        redirects.append([link, currLink])
    print(link + '|||' + currLink + '|||' + str(code))
    links.append([link + '|||' + currLink + '|||' + str(code)])
    df = df.append({'Original Link' : link, 'Redirected Link' : currLink, 'Code' : code, 'Dead Link' : dead_link}, ignore_index=True)
print(df)
df.to_excel(r'C:\Users\KitovYo\Desktop\Redirected_Sites.xlsx')