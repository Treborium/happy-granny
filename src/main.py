from unittest.mock import call
import requests
import json
import os

from typing import Union
from requests.models import Response
from bs4 import BeautifulSoup

from src.wollplatz import extract_wool_data


def main(extract_wool_data_fn: callable):
    input_data = {}
    with open("wool-input-data.json", "r") as input:
        input_data = json.load(input)

    wool_data = {generate_wool_id(wool): fetch_wool_data(wool, input_data["base_url"], extract_wool_data_fn)
                 for wool in input_data["wools"]}

    filename = "output/data.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w+") as outfile:
        json.dump(wool_data, outfile)


def generate_wool_id(wool) -> str:
    wool_id = f"{wool['brand']} {wool['description']}"
    return wool_id.replace(" ", "_")


# Possible improvement: Calls can be executed in parallel
def fetch_wool_data(wool, base_url: str, extract_wool_data_fn: callable) -> Union[dict, None]:
    wool_id = generate_wool_id(wool)

    page = fetch_wool_page(wool, base_url)
    if page.status_code == 200:
        dom = BeautifulSoup(page.content, "html.parser")
        wool_data = extract_wool_data_fn(dom)
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


if __name__ == "__main__":
    main(extract_wool_data)
