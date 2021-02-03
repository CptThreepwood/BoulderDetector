import os
import bs4
import json
import glob

def scrape_routes():
    routes = {}
    route_cache_file = os.path.join(OUT_DIR, 'all_routes.json')
    if os.path.exists(route_cache_file):
        with open(route_cache_file, 'r') as route_cache_io:
            routes = json.load(route_cache_io)
    for index in glob.glob(os.path.join(OUT_DIR, '*')):
        with open(index, 'r') as index_io:
            print(index)
            soup = bs4.BeautifulSoup(index_io, 'html.parser')
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
    scrape_routes()