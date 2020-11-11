import requests
import json
import orodja
import os
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

knjige = []
vrste = []

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
        
    print(f'Pridobivam knjige {start + 1} - {min(4920, start + stevilo_knjig_na_datoteko)}...')
    vsebina = orodja.knjige_splosne(url, zacetni_url, data, headers)
    knjige += vsebina

for knjiga in knjige:
    for posamezna_vrsta in knjiga['vrsta']:
        vrste.append({'knjiga': knjiga['naslov'], 'vrsta': posamezna_vrsta})
    del knjiga['vrsta']


orodja.zapisi_csv(knjige, ['izposoje', 'avtor', 'naslov', 'jezik'], os.path.join('podatki', 'knjige.csv'))
orodja.zapisi_csv(vrste, ['knjiga', 'vrsta'], os.path.join('podatki', 'vrste.csv'))
print('Shranjeni csv datoteki!')
