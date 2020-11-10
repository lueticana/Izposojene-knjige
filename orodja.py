import csv
import json
import os
import requests
import sys
import re
# datoteka pobrana z gradiv s predavanj ter prilagojena
# (spremenjena funkcija shrani_spletno_stran, dodana funkcija)

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

# prilagojena; response dobimo v json obliki, shranimo v json datoteko
def shrani_zacetno_spletno_stran_json(url, zacetni_url, ime_datoteke, data, headers, vsili_prenos=False):
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
        

#def shrani_spletno_stran(hash, ime_datoteke, headers, vsili_prenos=False):
#    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
#    #def odpri_cobiss_knjige(url, headers):
#    se = requests.Session()
#    zacetni_url = f'https://plus.cobiss.si/most-read-web/book/{hash}'
#    r = se.get(zacetni_url, headers=headers)
#    cobib_id = r.json()['data']['covivId']
#    url = f'https://plus.si.cobiss.net/opac7/bib/{cobib_id}'
#    try:
#        print('Shranjujem {} ...'.format(url), end='')
#        sys.stdout.flush()
#        if os.path.isfile(ime_datoteke) and not vsili_prenos:
#            print('shranjeno že od prej!')
#            return
#        r = requests.get(url)
#    except requests.exceptions.ConnectionError:
#        print('stran ne obstaja!')
#    else:
#        #pripravi_imenik(ime_datoteke)
#        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
#            datoteka.write(r.text)
#            print('shranjeno!')

def vsebina_json_datoteke(ime_datoteke):
    '''Vrne slovar json datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return json.load(datoteka)

def podrobnosti(knjiga, headers):
    '''b'''
    hash = knjiga['hash']
    url_knjige = f'https://plus.si.cobiss.net/most-read-web/rest/v1/books/group/list/?hash={hash}'
    se = requests.Session()
    r = se.get(url_knjige, headers=headers)
    cobib_id = r.json()['data'][0]['cobibId']
    cobiss_url = f'https://plus.si.cobiss.net/opac7/bib/{cobib_id}#full'
    ime_datoteke = os.path.join('podatki', str(cobib_id) + '.html')
    shrani_cobiss(cobiss_url, ime_datoteke)
    html = vsebina_datoteke(ime_datoteke)
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
    os.remove(ime_datoteke)
    return jezik, vrsta


def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding='utf-8') as datoteka:
        return datoteka.read()

def shrani_cobiss(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)




def shrani_zacetno_spletno_stran_json(url, zacetni_url, ime_datoteke, data, headers, vsili_prenos=False):
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
            vsebina = r.json()['data']
            for knjiga in vsebina:
                jezik, vrsta = podrobnosti(knjiga, headers)
                knjiga['izposoje'] = knjiga['totalCount']
                avtor = knjiga['author']
                avtor = avtor.split(',')
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
                
            json.dump(vsebina, datoteka, indent=4, ensure_ascii=False)
            print('shranjeno!')
        