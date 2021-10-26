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
   pip3 install -r requirements.txt
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

## Expected Input File Format

```
   "base_url": string,
   "wools": [
      { "brand": string, "description": string },
      ...
   ]
```

## Future Things to Consider

- [ ] execute https calls in parallel
- [ ] more robust error handling
- [ ] exhaustive unit tests
- [ ] type validation
- [ ] input sanitation
- [ ] pass input file as command line argument
