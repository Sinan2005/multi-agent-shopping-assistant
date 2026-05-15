import requests
from bs4 import BeautifulSoup

def scrape_reviews(url):

    try:

        response = requests.get(
            url,
            timeout=5
        )

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        return [
            t.get_text()
            for t in soup.find_all("p")[:5]
        ]

    except:
        return []