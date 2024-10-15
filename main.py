import requests
import webbrowser
from tqdm import tqdm
import time




def convert_to_url(search_term):
    status_code = 429
    while True:
        response = requests.get(
            f'https://api.semanticscholar.org/graph/v1/paper/search?query={search_term}')
        if response.status_code == 200:
            response_json = response.json()
            if "data" in response_json and response_json['data']:
                id = response_json['data'][0]['paperId']
                url = f"https://www.semanticscholar.org/paper/{id}"
                return url
            else:
                return None
        elif response.status_code == 429:
            time.sleep(2)
        else:
            return None
    
def get_urls(filename):
    filename = filename.replace('.txt', '') + '.txt'
    write_to = filename.split('.')[0] + "_urls.txt"
    search_terms_all = []
    with open(filename, 'r') as file:
        search_terms = file.readlines()
        for search_term in search_terms:
            search_term = search_term.strip()
            if search_term != '':
                search_terms_all.append(search_term)
    with open(write_to, 'w') as file:
        for search_term in tqdm(search_terms_all):
            url = convert_to_url(search_term)
            if url:
                file.write(url + '\n')
            else:
                file.write(f'{search_term}\n')


def open_urls(filename):
    filename = filename.replace('.txt', '') + '.txt'
    with open(filename, 'r') as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()
            if url != '':
                if url == "#":
                    return
                elif "https" in url:
                    webbrowser.open_new_tab(url)
    
if __name__ == '__main__':
    filenames = ["skim"]
    for filename in filenames:
        #get_urls(filename)
        pass
    open_urls(filenames[0].split('.')[0] + "_urls")