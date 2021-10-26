from unittest.mock import Mock, patch
from src.main import fetch_wool_data, generate_wool_id

import constants


def test_generate_wool_id():
    expected = "dmc_Natura_XL"
    assert generate_wool_id(constants.valid_wool) == expected


@patch('src.main.requests.get')
def test_fetch_wool_data(mock_get: Mock):
    with open(constants.html_file_path, "r") as html:
        mock_get.return_value.content = html
        mock_get.return_value.status_code = 200

        expected = {"Nadelstärke": "8 mm",
                    "Zusammenstellung": "100% Baumwolle",
                    "price": "7,92",
                    "stock_status": "available"}

        def extractor_fn(dom): return expected
        data = fetch_wool_data(constants.valid_wool,
                               constants.base_url, extractor_fn)
        assert data == expected


@patch('src.main.requests.get')
def test_fetch_invalid_wool_data(mock_get: Mock):
    mock_get.return_value.status_code = 404

    data = fetch_wool_data(constants.invalid_wool,
                           constants.base_url, lambda: "random-return-value")
    assert data == None
