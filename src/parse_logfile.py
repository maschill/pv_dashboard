#!/usr/bin/env python3

import numpy as np
import argparse
import sys
import os
import pytz

from tabulate import tabulate

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from datetime import timedelta
from datetime import datetime
from db_schemes import Messdaten

def localize_ts(ts):
    return pytz.timezone('Europe/Berlin').localize(datetime.utcfromtimestamp(ts))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="parse pv logfiles and write them to db")
    parser.add_argument("filename", metavar="filename", type=str, help="logfile that is parsed")
    parser.add_argument("-d", "--delete-old", dest="delete", action="store_true", help="delete all old records and write everything from the logfile to the db")
    parser.add_argument("-p", "--print-only", action="store_true", help="print parsed data instead of storing to DB")

    args = parser.parse_args()

    #fix some values
    wv = 300
    gu, gi, gp = 0,0,0
    wi, wu = 0,0
    
    dt = np.dtype([
        ('a', np.int16), # idk
        ('b', np.int16), # important for daily total/max/?? differentiation
        ('indicator', np.int32), # 6 for hourly
        ('timestamp', np.int32), # unix time in s
        ('value', np.int32) # in kwh*100
    ])

    with open(args.filename, 'rb') as fo:
        fo.seek(8)
        arr = np.fromfile(fo, dtype=dt, count=-1, sep='')

    if args.print_only:
        table = []
        for _a, b, ind, ts, val in arr:
            what_b = {
                    12290: 'total',
                    4149: 'peak',
                    4145: 'insulation',
                }
            table.append([localize_ts(ts), what_b.get(b, b), ind, val])

        print(tabulate(table, ["timestamp", "b", "type", "value"], tablefmt="grid"))
        sys.exit(0)

    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, 'db_config.txt'), 'r') as fo:
        connection = fo.read().strip()

    engine = create_engine(connection)

    last_inserted = [t[0] for t in engine.execute("SELECT coalesce(MAX(uhrzeit), to_timestamp(0)) FROM messdaten;")][0]
    print("inserting newer than ", last_inserted)

    if args.delete:
        engine.execute("DELETE FROM messdaten;")    

    wid = 4
    messdaten = []
    insert_time = datetime.now(pytz.timezone('Europe/Berlin'))
    for _a, _b, ind, ts, val in arr[1:]:
        t = localize_ts(ts)
        if t > last_inserted and ind == 6:
            messdaten.append(Messdaten(wid, t, timedelta(0,60,0), 0, gu, gi, gp, wu, wi, int(val), 30, insert_time))

    session = Session(bind=engine)
    print("created session")
    session.add_all(messdaten)
    session.commit()
