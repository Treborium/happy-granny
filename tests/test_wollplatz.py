from bs4 import BeautifulSoup

from src.wollplatz import extract_metadata, extract_price, extract_stock_status, extract_wool_data
import constants

# Only test happy path because of time constraint in challenge
def test_extract_wool_data() -> dict:
    with open(constants.html_file_path, "r") as html:
        dom = BeautifulSoup(html, constants.soup_parser)
        data = extract_wool_data(dom)

        expected = {"Nadelstärke": "8 mm",
                    "Zusammenstellung": "100% Baumwolle",
                    "price": "7,92",
                    "stock_status": "available"}
        assert data == expected

def test_extract_price():
    with open(constants.html_file_path, "r") as html:
        dom = BeautifulSoup(html, constants.soup_parser)
        price = extract_price(dom)
        assert price == "7,92"


def test_extract_missing_price():
    with open(constants.empty_html_file_path, "r") as html:
        dom = BeautifulSoup(html, constants.soup_parser)
        price = extract_price(dom)
        assert price == None


def test_extract_stock_status_available():
    with open(constants.html_file_path, "r") as html:
        dom = BeautifulSoup(html, constants.soup_parser)
        status = extract_stock_status(dom)
        assert status == "available"


def test_extract_stock_status_unavailable():
    with open("tests/resources/stock-status-unavailable.html", "r") as html:
        dom = BeautifulSoup(html, constants.soup_parser)
        status = extract_stock_status(dom)
        assert status == "not available"


def test_extract_missing_stock_status():
    with open(constants.empty_html_file_path, "r") as html:
        dom = BeautifulSoup(html, constants.soup_parser)
        status = extract_stock_status(dom)
        assert status == None


def test_extract_metadata():
    with open(constants.html_file_path, "r") as html:
        dom = BeautifulSoup(html, constants.soup_parser)
        data = extract_metadata(dom)

        expected = {"Nadelstärke": "8 mm",
                    "Zusammenstellung": "100% Baumwolle"}
        assert data == expected


def test_extract_missing_metadata():
    with open(constants.html_file_path, "r") as html:
        dom = BeautifulSoup(html, constants.soup_parser)
        dom.find("td", string="Nadelstärke").replace_with("<td></td>")
        data = extract_metadata(dom)

        expected = {"Nadelstärke": None,
                    "Zusammenstellung": "100% Baumwolle"}
        assert data == expected
