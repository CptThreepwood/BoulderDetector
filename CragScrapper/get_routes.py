import os
import bs4
import glob
import time
import json
import requests

from get_route_index import OUT_DIR as INDEX_DIR

ROUTE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './raw/routes/')
if not os.path.exists(ROUTE_DIR):
    os.makedirs(ROUTE_DIR)

ROUTE_BASE = "https://www.thecrag.com/"

def get_route_page(rel_url, wait=1):
    url = ROUTE_BASE + str(rel_url)
    try:
        return requests.get(url, timeout=10).content
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
        print('timed out, retrying')
        time.sleep(wait)
        return get_route_page(rel_url, wait*2)

def get_route_url_list():
    with open(os.path.join(INDEX_DIR, 'all_routes.json')) as route_url_io:
        return json.load(route_url_io).values()

def get_route(url):
    local_route = os.path.join(ROUTE_DIR, os.path.basename(url) + '.html')
    if os.path.exists(local_route):
        return False
    print('Downloading route {0}'.format(url))
    route_content = get_route_page(url)

    with open(local_route, 'wb') as route_io:
        route_io.write(route_content)
    return True

if __name__ == '__main__':
    for url in get_route_url_list():
        if get_route(url):
            time.sleep(0.2)
