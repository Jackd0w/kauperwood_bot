from bs4 import BeautifulSoup
from decimal import Decimal
import xmltodict
import requests
import json
import re

url = 'https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=218a941a6f3162cc2c4a17258e4f390e'

def load_exchange():
    return json.loads(str(requests.get(url)[4:]))


def get_exchange(ccy_key):
    for exc in load_exchange():
        if ccy_key == exc['CharCode']:
            return exc
    return False


def get_exchanges(ccy_pattern):
    result = []
    ccy_pattern = re.escape(ccy_pattern) + '.*'
    for exc in load_exchange():
        if re.match(ccy_pattern, exc['CharCode'], re.IGNORECASE) is not None:
            result.append(exc)
    return result
    

