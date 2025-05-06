import requests
from bs4 import BeautifulSoup as bs

BASEURL = "https://letterboxd.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def is_valid_account(username: str) -> tuple[bool,bool]:
    #return (bool, bool) for (user name exists, has_watchlist)
    url = f"{BASEURL}/{username}/watchlist/page/1/"
    resp = requests.get(url, headers=HEADERS)
    if resp.status_code == 404:
        return False, False
    
    soup = bs(resp.text, "html.parser")
    items = soup.find_all("li", class_="poster-container")
    return True, bool(items)



