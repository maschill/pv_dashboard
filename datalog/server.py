#!/usr/bin/python3
# encoding: utf-8

import argparse
import json
import os
import socketserver
import sys

from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# module aus ../src holen
srcpath = os.path.realpath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.append(srcpath)
import db_schemes


BUFFER_SIZE = 8192


# def parse_timedelta(as_str):
#     fields = as_str.strip().split(':')
#     if len(fields) != 3:
#         return None
#     return timedelta(hours=int(fields[0]), minutes=int(fields[1]), seconds=int(fields[2]))

class DataLogServer(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(BUFFER_SIZE).strip()
        try:
            j = json.loads(self.data)
        except json.JSONDecodeError as e:
            print(e, file=sys.stderr)
            return

        try:
            messwert = db_schemes.Messdaten(**j)
        except TypeError as e:
            print(e, file=sys.stderr)
            return

        self.server.db_session.add(messwert)
        self.server.db_session.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Serial Line data collection server')
    parser.add_argument('--port', '-p', metavar='PORT', type=int, help='Listen-Port for the server', required=True)
    args = parser.parse_args()

    with open(os.path.join(srcpath, "db_config.txt")) as f:
        db_connection_string = f.read().strip()

    engine = create_engine(db_connection_string)
    session = Session(bind=engine)

    server = socketserver.TCPServer(('0.0.0.0', args.port), DataLogServer)
    server.db_session = session

    server.serve_forever()
