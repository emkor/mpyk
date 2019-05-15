# mpyk
Simple Python 3 CLI script for retrieving Wrocław MPK trams and buses real-time location

## prerequisites
- Unix, `make`, `git`, `python3` with `pip`

## quick start (global installation)
- setup:
    - `git clone https://github.com/emkor/mpyk.git && cd mpyk`
    - `sudo pip install -r requirements.txt && chmod u+x mpyk.py`
- usage:
    - `./mpyk.py --utc --csv myData.csv --log myLogs.log`
    - for continuous mode: `./mpyk.py --each 10 --utc --dir . --log myLogs.log`

## virtualenv-based setup
- `git clone https://github.com/emkor/mpyk.git && cd mpyk`
- `make venv`
- using virtualenv Python executable:
    - `.venv/mpyk/bin/python mpyk.py --utc --csv myData.csv --log myLogs.log`
- using virtualenv session:
    - `source .venv/mpyk/bin/activate`
    - `./mpyk.py --utc --csv myData.csv --log myLogs.log`
