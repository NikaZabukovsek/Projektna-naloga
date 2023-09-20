import re
import os
import csv

series_directory = 'podatki'
frontpage_filename = 'glavna.html'
csv_filename = 'serije.csv'

def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()
    
def page_to_series(page_content):
    vzorec_serija = '{"currentRank":\d+,.+?,"__typename":"ChartTitleEdge"}'
    return re.findall(vzorec_serija, page_content, flags = re.DOTALL)

vsebina = read_file_to_string(series_directory, frontpage_filename)
serije = page_to_series(vsebina)

def get_dict_from_series_block(block):
    serija = {}
    vzorec_naslov = '"titleText":{"text":"(.+?)","__typename":"TitleText"}'
    vzorec_začetek = '"releaseYear":{"year":(\d+)?,.+,"__typename":"YearRange"}'
    vzorec_ocena = '"ratingsSummary":{"aggregateRating":(\d?\.?\d?|null),"voteCount":\d*,"__typename":"RatingsSummary"}'
    vzorec_dolžina = '"runtime":({"seconds":(\d*),"__typename":"Runtime"}|null)'
    vzorec_število = '"episodes":{"episodes":{"total":(\d*),"__typename":"EpisodeConnection"},"__typename":"Episodes"}'
    vzorec_položaj = '"meterRanking":{"currentRank":(\d+),.+,"__typename":"TitleMeterRanking"}'

    try:
      naslov = re.search(vzorec_naslov, block, flags=re.DOTALL).group(1)
      začetek_predvajanja = re.search(vzorec_začetek, block, flags = re.DOTALL).group(1)
      splošna_ocena = re.search(vzorec_ocena, block, flags = re.DOTALL).group(1)
      povprečna_dolžina_epizode = re.search(vzorec_dolžina, block, flags = re.DOTALL).group(2)
      število_epizod = re.search(vzorec_število, block, flags = re.DOTALL).group(1)
      položaj_na_lestvici = re.search(vzorec_položaj, block, flags = re.DOTALL).group(1)
      
    except AttributeError:
        print(f"Nepopolni vzorci pri (čudni?) seriji\n{block}")
        raise

    serija["naslov"] = naslov
    serija["začetek predvajanja"] = začetek_predvajanja
    serija["splošna ocena"] = splošna_ocena
    serija["povprečna dolžina epizode (v sekundah)"] = povprečna_dolžina_epizode
    serija["število epizod"] = število_epizod
    serija["položaj na lestvici"] = položaj_na_lestvici

    def poberi_avtorje(niz):
        vzorec_avtor = re.compile(r'"text":"([^"]+)"', flags = re.DOTALL)
        avtorji = []
        for avtor in vzorec_avtor.finditer(niz):
            avtorji.append(avtor.group(1))
        return avtorji
    
    vzorec_avtorji = re.compile(r'"creators":\[(.*?)\]', flags = re.DOTALL)
    poišči_avtorja = vzorec_avtorji.search(block)
    if poišči_avtorja:
        avtorji = poišči_avtorja.group(1)
        serija["avtorji"] = poberi_avtorje(avtorji)
    else:
        serija["avtorji"] = None

    def poberi_žanre(niz):
        vzorec_žanr = re.compile(r'"text":"([^"]+)"', flags=re.DOTALL)
        žanri = []
        for žanr in vzorec_žanr.finditer(niz):
            žanri.append(žanr.group(1))
        return žanri
    
    vzorec_žanri = re.compile(r'"titleGenres":{"genres":\[(.*?)\]', flags=re.DOTALL)
    poišči_žanr = vzorec_žanri.search(block)
    if poišči_žanr:
        žanri = poišči_žanr.group(1)
        serija["žanri"] = poberi_žanre(žanri)
    else:
        serija["žanri"] = None

    


    return serija

for serija in serije:
    print(get_dict_from_series_block(serija))

def series_from_file(filename, directory):
    vsebina = read_file_to_string(directory, filename)
    serije = page_to_series(vsebina)
    slovarji = []
    for serija in serije:
        slovarji.append(get_dict_from_series_block(serija))
    return slovarji

series_from_file(frontpage_filename, series_directory)

def write_csv(fieldnames, rows, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return

def write_series_to_csv(series, directory, filename):
    assert series and (all(slovar.keys() == series[0].keys() for slovar in series))
    imena_stolpcev = sorted(series[0])
    write_csv(imena_stolpcev, series, directory, filename)

vsi_slovarji = series_from_file(frontpage_filename, series_directory)

write_series_to_csv(vsi_slovarji, "obdelani podatki", csv_filename)










