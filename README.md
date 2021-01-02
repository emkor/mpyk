# mpyk ![CI](https://github.com/emkor/mpyk/workflows/CI/badge.svg)
Simple Python 3 library for retrieving Wrocław MPK trams and buses real-time location

## installation
- `pip install mpyk`

## usage
```python
from typing import Any, Dict, List 
from mpyk import MpykClient, MpykTransLoc

client = MpykClient()

all_positions: List[MpykTransLoc] = client.get_all_positions()
print(all_positions[0])
# MpykTransLoc(kind='bus', line='131', course=16949195, timestamp=datetime.datetime(2021, 1, 2, 16, 31, 32), lat=51.115585, lon=17.074024)

raw_positions: List[Dict[str, Any]] = client.get_all_positions_raw()
print(raw_positions[0])
# {'name': '131', 'type': 'bus', 'y': 17.078085, 'x': 51.123753, 'k': 16949195}
```
- `timestamp` is UTC time of the moment of making request to MPK API, with precision down to seconds

## development
- see `Makefile`
