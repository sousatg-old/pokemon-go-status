import requests

from bs4 import BeautifulSoup

BASE_URL = 'http://cmmcd.com/PokemonGo/'

def get_pokengo_server_status():
    try:
        r = requests.get(BASE_URL)

        if r.status_code != 200:
            return "Online!"
            
        soup = BeautifulSoup( r.text, 'html.parser' )
        return soup.body.header.h2.font.text
    except:
        return "Online!"
