import numpy as np
import argparse
import sys

from tabulate import tabulate

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from datetime import timedelta
from datetime import datetime
from db_schemes import Messdaten

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="parse pv logfiles and write them to db")
    parser.add_argument("filename", metavar="filename", type=str, help="logfile that is parsed")
    parser.add_argument("-d", "--delete-old",dest="delete", action="store_true", help="delete all old records and write everything from the logfile to the db")
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
            formatted = datetime.fromtimestamp(ts).isoformat()
            what_b = {
                    12290: 'total',
                    4149: 'peak',
                    4145: 'insulation',
                }
            table.append([formatted, what_b.get(b, b), ind, val])

        print(tabulate(table, ["date/time", "b", "type", "value"], tablefmt="grid"))
        sys.exit(0)

    connection = None
    with open('src/db_config.txt', 'r') as fo:
        connection = fo.read().strip()
    
    engine = create_engine(connection)
    
    if args.delete:
        last_timestamp = 0
    else:
        last_timestamp = [t[0] for t in engine.execute("SELECT MAX(uhrzeit) FROM messdaten;")][0].timestamp()
        print("inserting newer than ",last_timestamp)

    wid = 4
    messdaten = []
    insert_time = datetime.now()
    for _a, _b, ind, ts, val in arr[1:]:
        if args.delete or ts > last_timestamp:
            t = datetime.fromtimestamp(ts)
            messdaten.append(Messdaten(wid, t, timedelta(0,60,0), 0, gu, gi, gp, wu, wi, int(val), 30, insert_time))
    
    if args.delete:
        engine.execute("DELETE FROM messdaten;")    
    
    session = Session(bind=engine)
    print("created session")
    session.add_all(messdaten)
    session.commit()
