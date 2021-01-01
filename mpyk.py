#!/usr/bin/env python3

import argparse
import logging
import time
from datetime import datetime
from os import path
from typing import List, Dict, Union, Optional

import pytz
import requests

API_URL = "https://mpk.wroc.pl/bus_position"
ALL_BUSES = ['a', 'c', 'd', 'k', 'n', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110',
             '111', '112', '113', '114', '115', '116', '118', '119', '120', '121', '122', '124', '125', '126', '127',
             '128', '129', '130', '131', '132', '133', '134', '136', '140', '141', '142', '144', '145', '146', '147',
             '148', '149', '150', '206', '240', '241', '243', '245', '246', '247', '248', '249', '250', '251', '253',
             '255', '257', '259', '319', '325', '602', '607', '609', '612', '715']
ALL_TRAMS = ['0l', '0p', 't4', 't9', 'zlt', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '14', '15', '17',
             '20', '23', '24', '31', '32', '33']
POLAND_TIMEZONE = pytz.timezone("Europe/Warsaw")
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
        logging.debug(f"Got API response: {response.status_code}")
        return response.json()
    else:
        raise ValueError(f"Error from API: {response.status_code}: {response.content}")


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
    api_response = call_api(trams=ALL_TRAMS, buses=ALL_BUSES)
    csv_lines = [_to_csv_row(request_time, line) for line in api_response]
    logging.debug(f"Retrieved {len(csv_lines)} lines of data, storing at: {csv_path}")
    _handle_output(csv_lines, csv_file=csv_path)
    total_time = (_get_curr_time(in_utc) - request_time).total_seconds()
    logging.info(f"Retrieved {len(csv_lines)} lines of data and stored in {total_time:.3f}s!")


def _setup_logger(level: int = logging.INFO, log_file: Optional[str] = None) -> None:
    if log_file is not None:
        log_directory = path.dirname(path.abspath(log_file))
        if path.exists(log_directory):
            logging.basicConfig(format='%(levelname)s | %(asctime)s UTC | %(message)s', level=level, filename=log_file)
        else:
            print(f"Can not create log file; directory {log_directory} does not exists; will use stdout!")
            logging.basicConfig(format='%(levelname)s | %(asctime)s UTC | %(message)s', level=level)
    else:
        logging.basicConfig(format='%(levelname)s | %(asctime)s UTC | %(message)s', level=level)
    logging.Formatter.converter = time.gmtime


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Get real-time location for Wroclaw MPK trams and buses')
    parser.add_argument("--each", type=float, default=None,
                        help="Enables continuous mode: number of seconds  between consecutive calls for location data")
    parser.add_argument("--dir", type=str, default=None,
                        help="In continuous mode: directory where daily files shall be stored; default: current dir")
    parser.add_argument("--csv", type=str, default=None,
                        help="Append data to given file (if exists) instead of printing to stdout")
    parser.add_argument("--log", type=str, default=None,
                        help="Log events to file instead of stdout")
    parser.add_argument("--utc", action='store_true',
                        help="Use UTC time for data instead of Poland time; logs are always in UTC")
    parser.add_argument("--debug", action='store_true', help="Increase log verbosity")
    return parser.parse_args()


def main(each_sec: Optional[int], data_dir: Optional[str],
         csv_path: Optional[str], log_path: Optional[str],
         in_utc: bool, debug: bool) -> None:
    _setup_logger(level=logging.INFO if not debug else logging.DEBUG, log_file=log_path)

    logging.debug("Retrieving bus and trams data...")
    if each_sec is not None:
        if each_sec < 0.5 or each_sec > 86400:
            raise ValueError("Argument each must have value between 0.5 and 86400")
        if csv_path is not None:
            raise ValueError("Argument csv must not be set in continuous mode")
        else:
            data_dir = data_dir if data_dir is not None and path.isdir(path.abspath(data_dir)) else path.abspath(".")
            while True:
                req_time = _get_curr_time(in_utc)
                csv_path = path.join(data_dir, req_time.date().isoformat() + ".csv")
                try:
                    _get_and_store(req_time, csv_path, in_utc)
                except Exception as e:
                    logging.warning(e)
                time.sleep(each_sec)
    else:
        try:
            req_time = _get_curr_time(in_utc)
            _get_and_store(req_time, csv_path, in_utc)
        except Exception as e:
            logging.error(e)
            exit(1)
    exit(0)


if __name__ == '__main__':
    args = _parse_args()
    main(args.each, args.dir, args.csv, args.log, args.utc, args.debug)
