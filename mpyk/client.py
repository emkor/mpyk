from datetime import datetime
from logging import Logger, getLogger
from typing import Dict, Any, List

import requests

from mpyk.model import MpykTransLoc

API_URL = "https://mpk.wroc.pl/bus_position"
API_REQUEST_TIMEOUT_SEC = 10.
ALL_BUSES = ['a', 'c', 'd', 'k', 'n', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
             '111', '112', '113', '114', '115', '116', '118', '119', '120', '121', '122', '124', '125', '126', '127',
             '128', '129', '130', '131', '132', '133', '134', '136', '140', '141', '142', '144', '145', '146', '147',
             '148', '149', '150', '206', '240', '241', '243', '245', '246', '247', '248', '249', '250', '251', '253',
             '255', '257', '259', '319', '325', '602', '607', '609', '612', '715']
ALL_TRAMS = ['0l', '0p', 't4', 't9', 'zlt', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '14', '15', '17',
             '20', '23', '24', '31', '32', '33']
PKG_NAME = 'mpyk'
API_RET_TYPE = List[Dict[str, Any]]


class MpykClient:
    def __init__(self, api_url: str = API_URL, api_timeout_sec: float = API_REQUEST_TIMEOUT_SEC,
                 logger: Logger = getLogger(PKG_NAME)):
        self.api_url = api_url
        self.api_timeout_sec = api_timeout_sec
        self.log = logger

    def get_all_positions(self) -> List[MpykTransLoc]:
        timestamp = datetime.utcnow().replace(microsecond=0)
        return self._parse_into_obj(self.get_all_positions_raw(), timestamp)

    def get_position(self, bus_lines: List[str], tram_lines: List[str]) -> List[MpykTransLoc]:
        timestamp = datetime.utcnow().replace(microsecond=0)
        return self._parse_into_obj(self.get_position_raw(bus_lines, tram_lines), timestamp)

    def get_all_positions_raw(self) -> API_RET_TYPE:
        return self.get_position_raw(bus_lines=ALL_BUSES, tram_lines=ALL_TRAMS)

    def get_position_raw(self, bus_lines: List[str], tram_lines: List[str]) -> API_RET_TYPE:
        return self._make_request({"busList[tram][]": sorted([str(t) for t in tram_lines]),
                                   "busList[bus][]": sorted([str(b) for b in bus_lines])})

    def _make_request(self, body: Dict) -> API_RET_TYPE:
        response = requests.post(url=self.api_url, data=body, timeout=self.api_timeout_sec)
        if response.ok:
            self.log.debug(f"Got API response: {response.status_code}")
            return response.json()
        else:
            raise ValueError(f"Error from API: {response.status_code} {str(response.content)}")

    def _parse_into_obj(self, responses: API_RET_TYPE, timestamp: datetime) -> List[MpykTransLoc]:
        return [MpykTransLoc.parse(raw_resp, timestamp) for raw_resp in responses]
