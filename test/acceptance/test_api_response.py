from mpyk import call_api
from mpyk.mpyk import ALL_TRAMS, ALL_BUSES

MIN_EXPECTED_POSITIONS_COUNT = 3
EXPECTED_KEYS = {"name", "type", "k", "x", "y"}


def test_should_receive_positions_upon_calling_api_as_library():
    resp = call_api(ALL_TRAMS, ALL_BUSES)
    assert resp, f"Got empty response from API: {resp}"
    assert len(resp) > MIN_EXPECTED_POSITIONS_COUNT, f"Got only {len(resp)} results from API: {resp}"
    assert all([k in resp[0].keys() for k in EXPECTED_KEYS]), f"API response contains missing keys: {resp[0].keys()}"
