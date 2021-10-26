import requests
import json
import os

from typing import Union
from requests.models import Response
from bs4 import BeautifulSoup

from src.utils import flatten


def main():
    input_data = { }
    with open("wool-input-data.json", "r") as input:
        input_data = json.load(input)

    wool_data = {generate_wool_id(wool): fetch_wool_data(wool, input_data["base_url"])
                 for wool in input_data["wools"]}

    filename = "output/data.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as outfile:
        json.dump(wool_data, outfile)


def generate_wool_id(wool) -> str:
    wool_id = f"{wool['brand']} {wool['description']}"
    return wool_id.replace(" ", "_")


# Possible improvement: Calls can be executed in parallel
def fetch_wool_data(wool, base_url: str) -> Union[dict, None]:
    wool_id = generate_wool_id(wool)

    page = fetch_wool_page(wool, base_url)
    if page.status_code == 200:
        dom = BeautifulSoup(page.content, "html.parser")
        wool_data = extract_wool_data(dom)
        print(f"{wool_id}=", wool_data)
        return wool_data
    else:
        print(f"{wool_id}= Page does not exist")
        return None


def fetch_wool_page(wool, base_url: str) -> Response:
    brand = wool['brand']
    formatted_description = wool['description'].lower().replace(' ', '-')
    subpath = f"wolle/{brand}/{brand}-{formatted_description}"
    url: str = base_url + subpath
    return requests.get(url)


def extract_wool_data(dom: BeautifulSoup) -> dict:
    return {
        "price": extract_price(dom),
        "stock_status": extract_stock_status(dom),
        **extract_metadata(dom)
    }


def extract_metadata(dom: BeautifulSoup) -> dict:
    required_metadata = ["Nadelstärke", "Zusammenstellung"]
    wool_specs_element = dom.find(id="pdetailTableSpecs")

    values = {}
    for id in required_metadata:
        # Possible Improvement: Could be made case insenstive by providing a custom matching function
        found_metadata = wool_specs_element.find("td", string=id)
        if found_metadata:
            value = found_metadata.find_next_sibling("td").contents
            values[id] = flatten(value) if len(value) == 1 else value
        else:
            values[id] = None

    return values


def extract_price(dom: BeautifulSoup) -> Union[str, None]:
    price_element = dom.find(class_="product-price-amount")
    if price_element:
        price = price_element.contents
        return flatten(price) if len(price) == 1 else price
    else:
        return None


def extract_stock_status(dom: BeautifulSoup) -> Union[str, None]:
    if dom.find(class_="stock-green"):
        return "available"
    elif dom.find(class_="stock-red"):
        return "not available"
    else:
        return None


if __name__ == "__main__":
    main()
