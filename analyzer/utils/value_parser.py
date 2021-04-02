import requests
from bs4 import BeautifulSoup

resp = requests.get("http://www.cbr.ru/scripts/XML_daily.asp")
soup = BeautifulSoup(resp.content, "xml")

