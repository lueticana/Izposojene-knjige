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
stevilo_knjig_na_datoteko = 3
# 1000 je najvec mozno

knjige = []
vrste = []

for start in range(0, 9, stevilo_knjig_na_datoteko):
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

    ime_datoteke = os.path.join('podatki', f'knjige-{start + 1}-{min(start + stevilo_knjig_na_datoteko, 4920)}.json')
    orodja.shrani_zacetno_spletno_stran_json(url, zacetni_url,ime_datoteke, data, headers)
    knjige += orodja.vsebina_json_datoteke(ime_datoteke)
    os.remove(ime_datoteke)



for knjiga in knjige:
    for posamezna_vrsta in knjiga['vrsta']:
        vrste.append({'knjiga': knjiga['naslov'], 'vrsta': posamezna_vrsta})
    del knjiga['vrsta']
knjige.sort(key=lambda knjige: (knjiga['izposoje'], knjiga['naslov']))
print(vrste)


#with open(os.path.join('podatki', 'knjige.json'), 'w', encoding='utf-8') as datoteka:
#    json.dump(knjige, datoteka, indent=4, ensure_ascii=False)


csv_knjige = os.path.join('podatki', 'knjige_csv.csv')
if os.path.isfile(csv_knjige):
    print('shranjeno že od prej!')
else:
    orodja.zapisi_csv(knjige, ['izposoje', 'avtor', 'naslov', 'jezik'], csv_knjige)

csv_vrste = os.path.join('podatki', 'vrste_csv.csv')
orodja.zapisi_csv(vrste, ['knjiga', 'vrsta'], csv_vrste)
