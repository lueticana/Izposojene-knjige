import requests
import json
import orodja
# orodja.py pobrana z gradiv s predavanj ter prilagojena

zacetni_url = "https://plus.cobiss.si/most-read-web/"
url = "https://plus.si.cobiss.net/most-read-web/rest/v1/books/search"
# koda za avtorizacijo pobrana 8.11.2020: main.6f4217f1.chunk.js - this._apiToken="..."
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    "Authorization": "oIbcKoWDDxMbcBuXsirXBZb6Re2run4q"
    }
stevilo_knjig_na_datoteko = 1000
# 1000 je najvec mozno

for start in range(0, 4920, stevilo_knjig_na_datoteko):
    data = {
        "libType":None,
        "libAcronym":"MKL",
        "pubType":1,
        "periodFrom":201910,
        "periodTo":202009,
        "publishYear":None,
        "targetGroups":[],
        "contentTypes":[],
        "materialTypes":["7"],
        "firstResult":start,
        "maxResult":stevilo_knjig_na_datoteko
        }
    ime_datoteke = f'podatki/knjige-{start + 1}-{min(start + stevilo_knjig_na_datoteko, 4920)}.json'
    orodja.shrani_spletno_stran(url, zacetni_url,ime_datoteke, data, headers)







#se = requests.Session()
#se.auth = ('user', 'pass')
#se.get("https://plus.cobiss.si/most-read-web/")
#r = se.post(url, json=data, headers=headers)
#print(r.text)