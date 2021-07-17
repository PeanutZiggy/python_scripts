import requests
import time
from datetime import datetime

bc_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
iftt_url = 'https://maker.ifttt.com/trigger/{}/with/key/b_GtwqUWX7MDHRg-OJiwNL'
bc_threshhold = 10000

def format_bitcoin_history(bc_history):
    rows = []
    for bc_price in bc_history:
        date = bc_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bc_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)
    return '<br>'.join(rows)

def get_latest_price():
    response = requests.get(bc_url)
    response_json = response.json()
    return float(response_json[0]['price_usd'])

def post_ifttt_webhook(event, value):
    data = {'value1' : value}
    ifttt_event_url = iftt_url.format(event)
    requests.post(ifttt_event_url, json=data)

def main():
    bc_history = []
    while True:
        price = get_latest_price()
        date = datetime.now()
        bc_history.append({'date' : date, 'price' : price})

        if price < bc_threshhold:
            post_ifttt_webhook('price_emergency', price)

        if len(bc_history) == 5:
            post_ifttt_webhook('price_update', format_bitcoin_history(bc_history))
            bc_history= []

        time.sleep(5 * 60)

if __name__ == '__main__':
    main()
