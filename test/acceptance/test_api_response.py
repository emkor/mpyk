from typing import Any, Dict, List

import pytest

from mpyk import MpykClient, ALL_TRAMS, ALL_BUSES

MIN_EXPECTED_POSITIONS_COUNT = 3
EXPECTED_KEYS = {"name", "type", "k", "x", "y"}


@pytest.fixture(scope="session")
def all_units_api_response() -> List[Dict[str, Any]]:
    client = MpykClient()
    return client.get_all_positions_raw()


def test_api_should_return_minimal_amount_of_data(all_units_api_response: List[Dict[str, Any]]):
    resp = all_units_api_response
    assert resp, f"Got empty response from API: {resp}"


def test_api_should_respond_with_known_format(all_units_api_response: List[Dict[str, Any]]):
    resp = all_units_api_response
    assert len(resp) > MIN_EXPECTED_POSITIONS_COUNT, f"Got only {len(resp)} results from API: {resp}"
    assert isinstance(resp, List), f"Expected response to be a list, but was {type(resp)}: {resp}"
    assert isinstance(resp[0], Dict), f"Expected response items to be dicts, but was {type(resp)}: {resp}"
    assert set(resp[0].keys()).issubset(EXPECTED_KEYS), f"API response contains missing keys: {resp[0].keys()}"


def test_api_should_return_no_unexpected_lines(all_units_api_response: List[Dict[str, Any]]):
    resp = all_units_api_response
    resp_tram_lines = {dp['name'] for dp in resp if dp['type'] == 'tram'}
    assert resp_tram_lines.issubset(ALL_TRAMS), f"API returned some unexpected tram lines: {resp_tram_lines}"

    resp_bus_lines = {dp['name'] for dp in resp if dp['type'] == 'bus'}
    assert resp_bus_lines.issubset(ALL_BUSES), f"API returned some unexpected bus lines: {resp_bus_lines}"
