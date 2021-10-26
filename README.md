# Happy Granny 👵

Happy Granny is a platform to compare wool prices from multiple vendors 🧶

## Requirements

- [Python3](https://www.python.org/downloads/)

## Getting Started

1. Create a new virtual environment (if not already done)

   ```sh
   python3 -m venv venv
   ```

2. Activate the virtual environment

   ```sh
   source venv/bin/activate
   ```

3. Install dependencies

   ```sh
   pip3 install -e .
   ```

## Run Application

Make sure you activated your virtual environment via `source venv/bin/activate`.
After that simply run:

```sh
python3 src/main.py
```

This will generate a file named `output/data.json`. The file contains the specified data about the desired wool.

## Run Unit Tests

```sh
pytest
```

## Development Details

### Expected Input File Format

```
   "base_url": string,
   "wools": [
      { "brand": string, "description": string },
      ...
   ]
```

### Add New Page

To get the wool data from another page you need to provide a new `extractor` function. The `extractor` function should be a callable with the following signature:

```python
 # returns desired values in a dict
def extractor(dom: BeautifulSoup) -> dict:
   # Implementation
```

To use the new `extractor` function it's necessary to pass the function pointer to the `main` function (see _Future Things to Consider_ section for possible improvement).

## Future Things to Consider

- [ ] execute https calls in parallel
- [ ] more robust error handling
- [ ] exhaustive unit tests
- [ ] type validation
- [ ] input sanitation
- [ ] pass input file as command line argument
- [ ] pass extractor as command line argument
