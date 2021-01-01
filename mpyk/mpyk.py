import logging
from datetime import datetime
from os import path
from typing import List, Dict, Union, Optional

import pytz

from mpyk import MpykClient

POLAND_TIMEZONE = pytz.timezone("Europe/Warsaw")
NULL_VAL = "null"


def _to_csv_row(call_time: datetime, json_resp: Dict[str, Union[str, float, int]]) -> str:
    return ";".join([call_time.replace(microsecond=0).isoformat(),
                     str(json_resp.get("type", NULL_VAL)), str(json_resp.get("name", NULL_VAL)),
                     str(json_resp.get("k", NULL_VAL)),
                     str(json_resp.get("x", NULL_VAL)), str(json_resp.get("y", NULL_VAL))])


def _handle_output(lines: List[str], csv_file: Optional[str] = None) -> None:
    if csv_file:
        csv_dir = path.dirname(path.abspath(csv_file))
        if path.exists(csv_dir):
            with open(path.abspath(csv_file), "a") as out_file:
                for l in lines:
                    out_file.write(l + "\n")
            logging.debug(f"Wrote {len(lines)} lines to {csv_file}")
        else:
            raise ValueError(f"Directory for storing CSV: {csv_dir} does not exist!")
    else:
        for l in lines:
            print(l)


def _get_curr_time(in_utc: bool) -> datetime:
    return datetime.utcnow() if in_utc else datetime.now(POLAND_TIMEZONE)


def _get_and_store(request_time: datetime, csv_path: str, in_utc: bool) -> None:
    client = MpykClient()
    api_response = client.get_all_positions_raw()
    csv_lines = [_to_csv_row(request_time, line) for line in api_response]
    logging.debug(f"Retrieved {len(csv_lines)} lines of data, storing at: {csv_path}")
    _handle_output(csv_lines, csv_file=csv_path)
    total_time = (_get_curr_time(in_utc) - request_time).total_seconds()
    logging.info(f"Retrieved {len(csv_lines)} lines of data and stored in {total_time:.3f}s!")
