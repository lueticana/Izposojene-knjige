import csv
import json
import os
import requests
import sys
# datoteka pobrana z gradiv s predavanj ter prilagojena

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

# prilagojena; response dobimo v json obliki, shranimo v json datoteko
def shrani_spletno_stran(url, zacetni_url, ime_datoteke, data, headers, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v  json datoteko z danim imenom.'''
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return

        se = requests.Session()
        se.get(zacetni_url)

    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        r = se.post(url, json=data, headers=headers)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            json.dump(r.json()['data'], datoteka, indent=4, ensure_ascii=False)
            print('shranjeno!')
        


def vsebina_datoteke(ime_datoteke):
    '''Vrne slovar json datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return json.loads(datoteka)


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


