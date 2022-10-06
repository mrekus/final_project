import json
import requests
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

FOREX_ENDPOINT = "https://api.frankfurter.app/latest"
PAIRS = config["API"]["pairs"].split(",")


def get_rates(pairs=None, endpoint=FOREX_ENDPOINT):
    """
    Grąžina valiutų kursus iš pairs sąrašo config.ini faile.
    Jei nepavyksta, default duoda tik EUR
    """
    if pairs is None:
        pairs = PAIRS
    try:
        rates = {"EUR": 1}
        for i in pairs[1:]:
            forex_payload = {"from": "EUR", "to": i}
            r = requests.get(endpoint, params=forex_payload)
            res = json.loads(r.text)
            rate = res["rates"][i]
            rates[i] = rate
        return rates, pairs
    except:
        rates = {"EUR": 1}
        pairs = ["EUR"]
        return rates, pairs
