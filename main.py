import data_download
import data
import os

def main(redownload=True, reparse=True):
    filename = f"glavna.html"
    pot_html = os.path.join(data.series_directory, filename)
    if redownload or not os.path.exists(pot_html):
        data_download.save_frontpage(data_download.series_frontpage_url, data.series_directory, filename)
    else:
         print(f"Datoteka {pot_html} že obstaja")
    csv_mapa = "obdelani_podatki"
    pot_csv = os.path.join(csv_mapa, data.csv_filename)
   
    if reparse or not os.path.exists(pot_csv):
         vsi_slovarji = data.series_from_file(filename, data.series_directory)
         data.write_series_to_csv(vsi_slovarji, "obdelani_podatki", data.csv_filename)
    else:
        print(f"Datoteka {pot_csv} že obstaja")

          


