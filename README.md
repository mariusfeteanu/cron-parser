## Description
A command line application which parses a cron string and expands each field to show the times at which it will run. Example usage and output:

```
$ python cron_parser.py "*/15 0 1,2 * 1-5 /usr/bin/find"
minute               0 15 30 45
hour                 0
day of month         1  2
month                1  2  3  4  5  6  7  8  9 10 11 12
day of week          1  2  3  4  5
command             /usr/bin/find
```

## Prerequisites
- Python 3.8

## Set up

1. Create virtual environment:

```shell
python -m venv .env
source .env/bin/activate
```

2. Install dependencies
```shell
sudo pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Test

Unit tests
```shell
pytest --cov=. --cov-report term-missing test
```

Check style
```shell
flake8
pylint *.py
mypy
```

Run the command
```shell
python cron_parser.py "*/15 0 1,2 * 1-5 /usr/bin/find"
```

## Project structure:
- [mode](model.py): type definitions
- [input_output](input_output.py): read cron tables definitions from stdin and output time table details
- [field_tokenizer](field_tokenizer.py): interpret text fields into tokens to parse
- [field_parser](field_parser.py): parse a string of tokens into a time table
- [cron_parser](cron_parser.py): utility to read the cron tab from the cli and print the time table
- [test/](test/): tests
