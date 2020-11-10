import csv
import json
import os
import requests
import sys
import re
# datoteka pobrana z gradiv s predavanj, prilagojena ter dodanih nekaj orodij

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)
       


def podrobnosti(knjiga, headers):
    '''Generira url COBISS strani knjige, izlusci jezik in vrsto gradiva, nato html datoteko izbrise.'''
    hash = knjiga['hash']
    url_knjige = f'https://plus.si.cobiss.net/most-read-web/rest/v1/books/group/list/?hash={hash}'
    se = requests.Session()
    r = se.get(url_knjige, headers=headers)
    cobib_id = r.json()['data'][0]['cobibId']
    cobiss_url = f'https://plus.si.cobiss.net/opac7/bib/{cobib_id}#full'
    html = vsebina_cobiss_strani(cobiss_url)
    vzorec_za_jezik = re.compile(
        r'<span>Jezik</span> - \n\t*\n\t*(?P<jezik>.*?)\n',
        flags=re.DOTALL)
    vzorec_za_vrsto = re.compile(
        r'<span>Vrsta gradiva</span> - (?P<vrsta>[\w\W]*?)</div>',
        flags=re.DOTALL)
    jezik = vzorec_za_jezik.search(html)['jezik']
    vrsta = vzorec_za_vrsto.search(html)['vrsta']
    vrsta = vrsta.split(';')
    for i in range(len(vrsta)):
        vrsta[i] = vrsta[i].strip()
    #os.remove(ime_datoteke)
    return jezik, vrsta


def vsebina_cobiss_strani(url):
    '''Vrne vsebino strani na danem naslovu.'''
    try:
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print(f'stran {url} ne obstaja!')
    else:
        return r.text


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8', newline='') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


def knjige_splosne(url, zacetni_url, data, headers):
    '''Vrne precisceno vsebino strani kot seznam.'''
    try:
        se = requests.Session()
        se.get(zacetni_url)
    except requests.exceptions.ConnectionError:
        print(f'stran {zacetni_url} ne obstaja!')
    else:
        r = se.post(url, json=data, headers=headers)
        vsebina = r.json()['data']
        for knjiga in vsebina:
            jezik, vrsta = podrobnosti(knjiga, headers)
            knjiga['izposoje'] = knjiga['totalCount']
            avtor = knjiga['author']
            knjiga['avtor'] = avtor
            avtor = avtor.split(', ')
            if len(avtor) == 2:
                knjiga['avtor'] = avtor[1] + ' ' + avtor[0]
            knjiga['naslov'] = knjiga['descr']
            knjiga['jezik'] = jezik
            knjiga['vrsta'] = vrsta
            for key in [
                "cobibId",
                "hash",
                "hashHex",
                "publishYear",
                "contentType",
                "materialType",
                "targetGroup",
                "pubType",
                "hasNote",
                "descr",
                "author",
                "totalCount"
                ]:
                del knjiga[key]
    return vsebina
        