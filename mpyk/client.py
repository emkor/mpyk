from datetime import datetime
from logging import Logger, getLogger
from typing import Dict, Any, List

import requests

from mpyk.const import PKG_NAME, API_URL, API_REQUEST_TIMEOUT_SEC, ALL_TRAMS, ALL_BUSES
from mpyk.model import MpykTransLoc

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

    @classmethod
    def _parse_into_obj(cls, responses: API_RET_TYPE, timestamp: datetime) -> List[MpykTransLoc]:
        return [MpykTransLoc.parse(raw_resp, timestamp) for raw_resp in responses]
