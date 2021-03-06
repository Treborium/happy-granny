import os

test_dir = os.path.abspath(os.path.dirname(__file__))

html_file_path = f"{test_dir}/resources/wollplatz-dmc-natura-xl.html"
empty_html_file_path = f"{test_dir}/resources/empty.html"

base_url = "https://www.example.com/"
valid_wool = {"brand": "dmc", "description": "Natura XL"}
invalid_wool = {"brand": "invalid-brand", "description": "invalid-description"}
soup_parser = "html.parser"