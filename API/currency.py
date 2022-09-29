import json
import requests
import time


FOREX_ENDPOINT = "https://api.frankfurter.app/latest"
PAIRS = ["EUR", "USD", "GBP", "NOK"]


def get_rates(endpoint=FOREX_ENDPOINT):
    """
    Grąžina valiutų kursus iš PAIRS sąrašo
    """
    rates = {"EUR": 1}
    for i in PAIRS[1:]:
        forex_payload = {"from": "EUR", "to": i}
        r = requests.get(endpoint, params=forex_payload)
        res = json.loads(r.text)
        rate = res['rates'][i]
        rates[i] = rate
        time.sleep(0.5)
    return rates
