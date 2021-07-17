import requests
import xlrd
import pandas as pd
import time

from concurrent.futures import ProcessPoolExecutor



def main():
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

    # with ProcessPoolExecutor(max_workers=7) as e:
    #     e.map(test, range(1, 1802))
    #     e.map(test,range(1803, 2802))
    #     e.map(test,range(2803, 3802))
    #     e.map(test,range(3803, 4802))
    #     e.map(test,range(4803, 5802))
    #     e.map(test,range(5803, 6802))
    #     e.map(test,range(6803, 7802))
    with ProcessPoolExecutor(max_workers=7) as e:
        e.submit(test(1, 1802))
        e.submit(test(1803, 2802))
        e.submit(test(2803, 3802))
        e.submit(test(3803, 4802))
        e.submit(test(4803, 5802))
        e.submit(test(5803, 6802))
        e.submit(test(6803, 7802))

    print(df)
    df.to_excel(r'C:\Users\KitovYo\Desktop\Redirected_Sites_Multiprocessed.xlsx')


# it doesnt work in general because it is calling separate instances of the function all creating a new df
# at the end their results are not merging 
# instead do this:
# try running it as a single link checker and return the result from which you add to a dic and then transform the dic to df



def test(one, two, dff):
    # l = []
    # for i in one:
    #     l.append(i)

    # print(l)
    for site in range(one, two):
        weblink = dff.cell(site, 0).value # change the 0 to the column that you are using
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
        print(link + ' ||| ' + currLink + ' ||| ' + str(code))
        links.append([link + ' ||| ' + currLink + ' ||| ' + str(code)])
        df = df.append({'Original Link' : link, 'Redirected Link' : currLink, 'Code' : code, 'Dead Link' : dead_link}, ignore_index=True)

if __name__ == '__main__':
    main()