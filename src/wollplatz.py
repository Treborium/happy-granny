from typing import Union
from bs4 import BeautifulSoup

from src.utils import flatten

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
