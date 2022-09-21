
import requests

def load_lottieur(url):
    r=requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

