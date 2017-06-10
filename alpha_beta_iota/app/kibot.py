import csv
import requests

KIBOT_HISTORY_URL_BASE = 'http://api.kibot.com/?action=history&splitadjusted=1'

def kibot_fetch_history(symbol, interval, period):
    url = KIBOT_HISTORY_URL_BASE + '&symbol={}&interval={}&period={}'.format(
        symbol, interval, period
    )

    resp = requests.get(url)
    if resp.text == '401 Not Logged In':
        requests.get('http://api.kibot.com/?action=login&user=guest&password=guest')
        resp = requests.get(url)

    if resp.status_code != 200:
        raise Exception('Error calling kibot. Got status code: ' + resp.status_code)

    fieldnames = ['dt', 'o', 'h', 'l', 'c', 'vol']
    reader = csv.DictReader(resp.text.split('\n'), fieldnames=fieldnames)
    return list(reader)
