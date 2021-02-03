import os
import bs4
import glob
from parse_route_urls import ROUTE_DIR

def parse_route_page(id, html):
    soup = bs4.BeautifulSoup(html)

    def get_rating(label):
        element = soup.find('tr', title=lambda x: rating in x if x else False)
        try:
            return int(element['title'].split()[0])
        except Exception as err:
            raise(err)
    
    return {
        'lat': float(soup.find('meta', property="place:location:latitude")['content']),
        'lon': float(soup.find('meta', property="place:location:longitude")['content']),
        'name': groupings[-1],
        'id': id
        'groupings': groupings,
        'ratings': {
            1: get_rating('Crap'),
            2: get_rating("Don't Bother"),
            3: get_rating('Average'),
            4: get_rating('Good'),
            5: get_rating('Very Good'),
            6: get_rating('Classic'),
            7: get_rating('Mega Classic'),
        },
        'tags': [tag.text for tag in soup.find_all('a', rel='tag')],
    }

def parse_routes():
    route_data = {}
    for route_page in glob.glob(os.path.join(ROUTE_DIR, '*.html')):
        i = os.path.basename(route_page).split('.')[0]
        with open(route_page) as route_io:
            route_data[i] = parse_route_page(i, route_io.read())
    with open(os.path.join(ROUTE_DIR, 'route_data.json')) as route_data_io:
        json.dump(route_data, route_data_io)
