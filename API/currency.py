import json
import requests


FOREX_ENDPOINT = "https://api.frankfurter.app/latest"
PAIRS = [["EUR", "USD"], ["EUR", "GBP"], ["EUR", "NOK"]]


def get_rates(endpoint=FOREX_ENDPOINT):
    """
    Grąžina valiutų kursus iš PAIRS sąrašo
    """
    rates = {"EUR": 1}
    for i in PAIRS:
        forex_payload = {"from": i[0], "to": i[1]}
        r = requests.get(endpoint, params=forex_payload)
        res = json.loads(r.text)
        rate = res['rates'][i[1]]
        rates[i[1]] = rate
    return rates
