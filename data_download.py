import requests
import os

series_frontpage_url = 'https://www.imdb.com/chart/tvmeter/'  
series_directory = 'podatki'
frontpage_filename = 'glavna.html'
 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


def download_url_to_string(url):
    try:
        page_content = requests.get(url, headers=headers)
        if page_content.status_code == 200:
            return page_content.text
        else:
            raise ValueError(f"Čudna koda: {page_content.status_code}")
    except Exception:
        print("Prišlo je do nekakšne napake, prekinjam izvajanje.")

def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None

def save_frontpage(page, directory, filename):
    html_strani = download_url_to_string(page)
    save_string_to_file(html_strani, directory, filename)

save_frontpage(series_frontpage_url, series_directory, frontpage_filename)
 




