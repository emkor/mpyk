import argparse
import logging
import time
from os import path
from typing import Optional

from mpyk.mpyk import _get_curr_time, _get_and_store


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
            data_dir = data_dir if data_dir is not None and path.isdir(path.abspath(data_dir)) else path.abspath("..")
            while True:
                req_time = _get_curr_time(in_utc)
                csv_path = path.join(data_dir, req_time.date().isoformat() + ".csv")
                try:
                    _get_and_store(req_time, csv_path, in_utc)
                except Exception as e:
                    logging.warning(e)
                time.sleep(each_sec)
    else:
        if csv_path is None:
            raise ValueError(f"Given path to csv file is empty: {csv_path}")
        try:
            req_time = _get_curr_time(in_utc)
            _get_and_store(req_time, csv_path, in_utc)
        except Exception as e:
            logging.error(e)
            exit(1)
    exit(0)


def cli_main():
    args = _parse_args()
    main(args.each, args.dir, args.csv, args.log, args.utc, args.debug)


if __name__ == '__main__':
    cli_main()
