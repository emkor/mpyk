# mpyk
Simple Python 3 CLI script for retrieving Wrocław MPK trams and buses real-time location

## prerequisites
- Unix, `python3` with `pip`, `make` tool

## quick start (global installation)
- `git clone https://github.com/emkor/mpyk.git && cd mpyk`
- `sudo pip install -r requirements.txt && chmod u+x mpyk.py`
- `mpyk.py --utc --csv myData.csv --log myLogs.log`

## virtualenv-based setup
- `git clone https://github.com/emkor/mpyk.git && cd mpyk`
- `make config`
- using virtualenv Python executable:
    - `.venv/mpyk/bin/python mpyk.py --utc --csv myData.csv --log myLogs.log`
- using virtualenv session:
    - `source .venv/mpyk/bin/activate`
    - `mpyk.py --utc --csv myData.csv --log myLogs.log`
