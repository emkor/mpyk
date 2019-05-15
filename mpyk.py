#!/usr/bin/env python3

import argparse
import logging
import time
from datetime import datetime
from os import path
from typing import List, Dict, Union, Optional

import requests

API_URL = "http://mpk.wroc.pl/position.php"
ALL_BUSES = ['a', 'c', 'd', 'k', 'n', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
             '111', '112', '113', '114', '115', '116', '118', '119', '120', '121', '122', '124', '125', '126', '127',
             '128', '129', '130', '131', '132', '133', '134', '136', '140', '141', '142', '144', '145', '146', '147',
             '148', '149', '150', '206', '240', '241', '243', '245', '246', '247', '248', '249', '250', '251', '253',
             '255', '257', '259', '319', '325', '602', '607', '609', '612', '715']
ALL_TRAMS = ['0l', '0p', 't4', 't9', 'zlt', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '14', '15', '17',
             '20', '23', '24', '31', '32', '33']

NULL_VAL = "null"


def call_api(trams: Optional[List[str]] = None,
             buses: Optional[List[str]] = None) -> List[Dict[str, Union[str, float, int]]]:
    if not trams and not buses:
        raise ValueError("Can not call API without any parameters!")

    req_body = {}
    if trams:
        req_body["busList[tram][]"] = sorted([str(t) for t in trams])
    if buses:
        req_body["busList[bus][]"] = sorted([str(b) for b in buses])

    response = requests.post(url=API_URL, data=req_body)
    if response.ok:
        return response.json()
    else:
        raise ValueError(f"Error from API: {response.status_code}: {response.content}")


def to_csv_row(call_time: datetime, json_resp: Dict[str, Union[str, float, int]]) -> str:
    return ";".join([call_time.isoformat(),
                     json_resp.get("type", NULL_VAL), json_resp.get("name", NULL_VAL),
                     str(json_resp.get("k", NULL_VAL)),
                     str(json_resp.get("x", NULL_VAL)), str(json_resp.get("y", NULL_VAL))])


def handle_output(lines: List[str], csv_file: [Optional[str]] = None) -> None:
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


def _setup_logger(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    if log_file is not None:
        log_directory = path.dirname(path.abspath(log_file))
        if path.exists(log_directory):
            logging.basicConfig(format='%(levelname)s | %(asctime)s UTC | %(message)s', level=level, filename=log_file)
        else:
            print("Can not create log file; directory {} does not exists; will use stdout!".format(log_directory))
            logging.basicConfig(format='%(levelname)s | %(asctime)s UTC | %(message)s', level=level)
    else:
        logging.basicConfig(format='%(levelname)s | %(asctime)s UTC | %(message)s', level=level)
    logging.Formatter.converter = time.gmtime


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Get real-time location for Wroclaw MPK trams and buses')
    parser.add_argument("--csv", type=str, default=None,
                        help="Append data to given file (if exists) instead of printing to stdout")
    parser.add_argument("--log", type=str, default=None,
                        help="Log events to file instead of stdout")
    parser.add_argument("--utc", action='store_true', help="Use UTC time for data")
    parser.add_argument("--debug", action='store_true', help="Increase log verbosity")
    return parser.parse_args()


def cli_main() -> None:
    args = _parse_args()
    _setup_logger(level=logging.INFO if not args.debug else logging.DEBUG, log_file=args.log)
    request_time = datetime.utcnow() if args.utc else datetime.now()
    try:
        api_response = call_api(trams=ALL_TRAMS, buses=ALL_BUSES)
        csv_lines = [to_csv_row(request_time, line) for line in api_response]
        handle_output(csv_lines, csv_file=args.csv)
        total_time = ((datetime.utcnow() if args.utc else datetime.now()) - request_time).total_seconds()
        logging.info(f"Retrieved and stored data in {total_time}s!")
    except Exception as e:
        logging.error(f"{e}")
        exit(1)
    exit(0)


if __name__ == '__main__':
    cli_main()
