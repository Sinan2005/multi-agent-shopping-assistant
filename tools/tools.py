import requests
import os

def search_products(query):

    print("Searching:", query)

    url = "https://serpapi.com/search.json"

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY")
    }

    response = requests.get(
        url,
        params=params
    )

    data = response.json()

    shopping_results = data.get(
        "shopping_results",
        []
    )

    products = []

    for r in shopping_results[:5]:

        products.append({
            "name": r.get("title"),
            "price": r.get("price"),
            "rating": r.get("rating"),
            "link": r.get("product_link"),
            "image": r.get("thumbnail")
        })

    print("Products extracted:", len(products))

    return products