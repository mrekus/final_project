import json
import requests


FOREX_ENDPOINT = "https://api.frankfurter.app/latest"
PAIRS = [
    "EUR",
    "USD",
    "NOK",
    "GBP",
]  # pirmas turi likti EUR kaip default, pridėtus naujų programa updatina automatiškai


def get_rates(endpoint=FOREX_ENDPOINT):
    """
    Grąžina valiutų kursus iš PAIRS sąrašo
    """
    rates = {"EUR": 1}
    for i in PAIRS[1:]:
        forex_payload = {"from": "EUR", "to": i}
        r = requests.get(endpoint, params=forex_payload)
        res = json.loads(r.text)
        rate = res["rates"][i]
        rates[i] = rate
    return rates
