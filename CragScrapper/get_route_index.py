import os
import bs4
import glob
import time
import requests

from urllib.parse import urlparse, parse_qs

OUT_DIR = "./index/"
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

INDEX_BASE = "https://www.thecrag.com/en/climbing/world/routes"
INDEX_PAGE = INDEX_BASE + '?page='

def get_index_page(page_no):
    url = INDEX_PAGE + str(page_no)
    return requests.get(url).content

def parse_link(url):
    print(url)
    return int(parse_qs(urlparse(url).query)['page'][0])

def parse_next_page(content):
    soup = bs4.BeautifulSoup(content, features='html.parser')
    return [
        parse_link(x['href'])
        for x in soup.find_all('a')
        if 'Next' in x.text and 'page' in x['href']
    ]

def save_index_page(page_no):
    print('Downloading index {0}'.format(page_no))
    index_content = get_index_page(page_no)

    with open(os.path.join(OUT_DIR, "{0}.html".format(page_no)), 'wb') as index_file:
        index_file.write(index_content)
    
    indices = parse_next_page(index_content)
    next_index = min(i for i in indices if i > page_no) if indices else None
    if next_index:
        time.sleep(1)
        save_index_page(next_index)

def get_id(url):
    return int(url.split('/')[-1])

def scrape_routes():
    routes = {}
    route_cache_file = os.path.join(OUT_DIR, 'all_routes.sjon')
    if os.path.exists(route_cache_file):
        with open(route_cache_file, 'r') as route_cache_io:
            routes = json.load(route_cache_io)
    for index in glob.glob(os.path.join(OUT_DIR, '*')):
        with open(index, 'r') as index_io:
            soup = bs4.BeautifulSoup(index_io)
            routes.update({
                get_id(link['href']): link['href']
                for link in soup.find_all('a')
                if 'href' in link.attrs
                and '/route/' in link['href']
                and not link['href'].endswith('ascents')
            })
    with open(route_cache_file, 'w') as route_cache_io:
        json.dump(routes, route_cache_io)
    return routes


if __name__ == "__main__":
    # cached = glob.glob(os.path.join(OUT_DIR, '*.html'))
    # indices = [int(os.path.basename(x)[:-5]) for x in cached]
    # save_index_page(max(indices) if indices else 1)
    scrape_routes()

