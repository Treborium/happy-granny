from bs4 import BeautifulSoup
from src.main import extract_metadata, extract_price, extract_stock_status, extract_wool_data, fetch_wool_data, generate_wool_id

from unittest.mock import Mock, patch


html_file_path = "tests/resources/wollplatz-dmc-natura-xl.html"
empty_html_file_path = "tests/resources/empty.html"

base_url = "https://www.example.com/"
valid_wool = {"brand": "dmc", "description": "Natura XL"}
invalid_wool = {"brand": "invalid-brand", "description": "invalid-description"}
soup_parser = "html.parser"


def test_generate_wool_id():
    expected = "dmc_Natura_XL"
    assert generate_wool_id(valid_wool) == expected


@patch('src.main.requests.get')
def test_fetch_wool_data(mock_get: Mock):
    with open(html_file_path, "r") as html:
        mock_get.return_value.content = html
        mock_get.return_value.status_code = 200

        expected = {"Nadelstärke": "8 mm",
                    "Zusammenstellung": "100% Baumwolle",
                    "price": "7,92",
                    "stock_status": "available"}
        data = fetch_wool_data(valid_wool, base_url)
        assert data == expected


@patch('src.main.requests.get')
def test_fetch_invalid_wool_data(mock_get: Mock):
    mock_get.return_value.status_code = 404

    data = fetch_wool_data(invalid_wool, base_url)
    assert data == None


def test_extract_price():
    with open(html_file_path, "r") as html:
        dom = BeautifulSoup(html, soup_parser)
        price = extract_price(dom)
        assert price == "7,92"


def test_extract_missing_price():
    with open(empty_html_file_path, "r") as html:
        dom = BeautifulSoup(html, soup_parser)
        price = extract_price(dom)
        assert price == None


def test_extract_stock_status_available():
    with open(html_file_path, "r") as html:
        dom = BeautifulSoup(html, soup_parser)
        status = extract_stock_status(dom)
        assert status == "available"


def test_extract_stock_status_unavailable():
    with open("tests/resources/stock-status-unavailable.html", "r") as html:
        dom = BeautifulSoup(html, soup_parser)
        status = extract_stock_status(dom)
        assert status == "not available"


def test_extract_missing_stock_status():
    with open(empty_html_file_path, "r") as html:
        dom = BeautifulSoup(html, soup_parser)
        status = extract_stock_status(dom)
        assert status == None


def test_extract_metadata():
    with open(html_file_path, "r") as html:
        dom = BeautifulSoup(html, soup_parser)
        data = extract_metadata(dom)

        expected = {"Nadelstärke": "8 mm",
                    "Zusammenstellung": "100% Baumwolle"}
        assert data == expected


def test_extract_missing_metadata():
    with open(html_file_path, "r") as html:
        dom = BeautifulSoup(html, soup_parser)
        dom.find("td", string="Nadelstärke").replace_with("<td></td>")
        data = extract_metadata(dom)

        expected = {"Nadelstärke": None,
                    "Zusammenstellung": "100% Baumwolle"}
        assert data == expected


# Only test happy path because of time constraint in challenge
def test_extract_wool_data() -> dict:
    with open(html_file_path, "r") as html:
        dom = BeautifulSoup(html, soup_parser)
        data = extract_wool_data(dom)

        expected = {"Nadelstärke": "8 mm",
                    "Zusammenstellung": "100% Baumwolle",
                    "price": "7,92",
                    "stock_status": "available"}
        assert data == expected
