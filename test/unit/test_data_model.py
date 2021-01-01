import json
from datetime import datetime
from decimal import Decimal

from mpyk.model import MpykTransLoc

API_RESPONSE = [
    {'name': '0l', 'type': 'tram', 'y': 17.030212, 'x': 51.118153, 'k': 16952122},
    {'name': '145', 'type': 'bus', 'y': 17.036057, 'x': 51.099934, 'k': 16972856},
    {'name': '148', 'type': 'bus', 'y': 16.872084, 'x': 51.145226, 'k': 16972952},
    {'name': '10', 'type': 'tram', 'y': 16.871788, 'x': 51.144512, 'k': 16952632},
    {'name': '145', 'type': 'bus', 'y': 17.058632, 'x': 51.05095, 'k': 16972837},
    {'name': '112', 'type': 'bus', 'y': 17.006483, 'x': 51.0746, 'k': 16971472},
    {'name': '128', 'type': 'bus', 'y': 17.041739, 'x': 51.117012, 'k': 16972274},
    {'name': '0l', 'type': 'tram', 'y': 17.044817, 'x': 51.12415, 'k': 16952099},
    {'name': '128', 'type': 'bus', 'y': 17.125038, 'x': 51.16268, 'k': 16972290},
    {'name': '148', 'type': 'bus', 'y': 16.920029, 'x': 51.123394, 'k': 16973003},
    {'name': '148', 'type': 'bus', 'y': 17.039347, 'x': 51.100567, 'k': 16972970},
    {'name': '128', 'type': 'bus', 'y': 16.948362, 'x': 51.13654, 'k': 16972313},
    {'name': '148', 'type': 'bus', 'y': 16.886852, 'x': 51.141052, 'k': 16972987},
    {'name': '149', 'type': 'bus', 'y': 17.063763, 'x': 51.112732, 'k': 16973077},
    {'name': '128', 'type': 'bus', 'y': 17.032595, 'x': 51.11707, 'k': 16972259},
    {'name': '612', 'type': 'bus', 'y': 17.031599, 'x': 51.094536, 'k': 16971556},
    {'name': '145', 'type': 'bus', 'y': 17.06464, 'x': 51.109894, 'k': 16972817},
    {'name': '149', 'type': 'bus', 'y': 16.963629, 'x': 51.113354, 'k': 16973022},
    {'name': '612', 'type': 'bus', 'y': 17.032536, 'x': 51.072033, 'k': 16971514},
    {'name': '32', 'type': 'tram', 'y': 16.981836, 'x': 51.130333, 'k': 16953017},
    {'name': '11', 'type': 'tram', 'y': 17.047285, 'x': 51.126427, 'k': 16953277},
    {'name': '31', 'type': 'tram', 'y': 17.022385, 'x': 51.104267, 'k': 16953078},
    {'name': '32', 'type': 'tram', 'y': 17.045416, 'x': 51.077168, 'k': 16953139},
    {'name': '33', 'type': 'tram', 'y': 16.971666, 'x': 51.129467, 'k': 16952195},
    {'name': '32', 'type': 'tram', 'y': 17.011862, 'x': 51.11292, 'k': 16953039},
    {'name': '31', 'type': 'tram', 'y': 17.03425, 'x': 51.09393, 'k': 16953117},
    {'name': '11', 'type': 'tram', 'y': 16.99346, 'x': 51.097885, 'k': 16953257},
    {'name': '31', 'type': 'tram', 'y': 16.966167, 'x': 51.13838, 'k': 16953155},
    {'name': '32', 'type': 'tram', 'y': 17.039345, 'x': 51.077255, 'k': 16953059},
    {'name': '24', 'type': 'tram', 'y': 16.995821, 'x': 51.089985, 'k': 16952755},
    {'name': '8', 'type': 'tram', 'y': 17.03671, 'x': 51.128513, 'k': 16953642},
    {'name': '23', 'type': 'tram', 'y': 17.036352, 'x': 51.107513, 'k': 16953193},
    {'name': '10', 'type': 'tram', 'y': 17.059063, 'x': 51.111687, 'k': 16952586},
    {'name': '11', 'type': 'tram', 'y': 17.036192, 'x': 51.10079, 'k': 16953297},
    {'name': '23', 'type': 'tram', 'y': 17.066008, 'x': 51.132145, 'k': 16953216},
    {'name': '23', 'type': 'tram', 'y': 16.987667, 'x': 51.12377, 'k': 16953318},
    {'name': '33', 'type': 'tram', 'y': 17.070377, 'x': 51.114456, 'k': 16952214},
]


def test_should_parse_api_resp_into_objects():
    ts = datetime.utcnow()
    output = []
    for raw_transloc in API_RESPONSE:
        transloc = MpykTransLoc.parse(raw_transloc, ts)
        assert transloc is not None, f"Could not parse {raw_transloc} into meaningful object"
        output.append(transloc)
    assert output[0] == MpykTransLoc('tram', '0l', 16952122, ts, Decimal(51.118153), Decimal(17.030212))


def test_should_serialize_object():
    ts = datetime(2021, 1, 1, 22, 6, 9, 101)
    obj = MpykTransLoc('tram', '0l', 16952122, ts, Decimal(51.118153), Decimal(17.030212))
    assert obj.as_api_dict() == {'name': '0l', 'type': 'tram', 'y': 17.030212, 'x': 51.118153, 'k': 16952122}
    assert json.dumps(obj.as_api_dict()) is not None
    assert obj.as_dict() == {'line': '0l', 'kind': 'tram', 'lon': 17.030212, 'lat': 51.118153, 'course': 16952122,
                             'timestamp': '2021-01-01T22:06:09'}
    assert json.dumps(obj.as_dict()) is not None
    assert obj.as_values() == ('2021-01-01T22:06:09', 'tram', '0l', 16952122, 51.118153, 17.030212)
