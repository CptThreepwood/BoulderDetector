import os
import bs4
import glob
import time
import requests

import OUT_DIR from get_route_index as INDEX_DIR
ROUTE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './raw/routes/')
if not os.path.exists(ROUTE_DIR):
    os.makedirs(ROUTE_DIR)

ROUTE_BASE = "https://www.thecrag.com/"

def get_route_page(rel_url):
    url = ROUTE_BASE + str(rel_url)
    return requests.get(url).content

def get_route_url_list():
    with open(os.path.join(INDEX_DIR, 'all_routes.json')) as route_url_io:
        return json.load(route_url_io).values()

def get_route(url):
    local_route = os.path.join(ROUTE_DIR, os.path.basename(url))
    if os.path.exists(local_route):
        return
    print('Downloading route {0}'.format(url))
    route_content = get_route_page(url)

    with open(local_route, 'wb') as route_io:
        route_io.write(route_content)

if __name__ == '__main__':
    for url in get_route_url_list():
        get_route(url)
        time.sleep(1)
