import telebot
import datetime
import json
from logging import getLogger
from collections import namedtuple
import xmltodict
import requests

logger = getLogger(__name__)

Rate = namedtuple('Rate', 'name,rate')

def str_to_float(item: str) -> float:
    item = item.replace(',', '.')
    return float(item)



def get_rates(section_id):
    get_url = "http://www.cbr.ru/scripts/XML_daily.asp?"
    date_format = "%d/%m/%Y"

    today = datetime.datetime.today()
    params = {
        "date_req": today.strftime(date_format),
    }
    r = requests.get(get_url, params=params)
    resp = r.text 
    print(resp)

    data = xmltodict.parse(resp)
    print(json.dumps(data, indent = 2))

    rate = None
    currency_name = None

    for item in data['ValCurs']['Valute']:
        if item['@ID'] == section_id:
            r = Rate(
                name = item['CharCode'],
                rate = str_to_float(item['Value'])
            )
            
            print(r)
            return(r)
            break
