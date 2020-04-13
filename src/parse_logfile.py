import numpy as np
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from datetime import timedelta
from datetime import datetime
from db_schemes import Messdaten

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python parse_logfile.py <filename>")
        exit(0)
    
    #fix some values
    wv = 300
    gu, gi, gp = 0,0,0
    wi, wu = 0,0
    
    filename = sys.argv[1]

    dt = np.dtype([
        ('a', np.int32), # idk
        ('indicator', np.int32), # 6 for hourly
        ('timestamp', np.int32), # unix time in s
        ('value', np.int32) # in kwh*100
    ])

    with open(filename, 'rb') as fo:
        fo.seek(8)
        arr = np.fromfile(fo, dtype=dt, count=-1, sep='')

    connection = None
    with open('src/db_config.txt', 'r') as fo:
        connection = fo.read().strip()
    
    engine = create_engine(connection)

    wid = 4
    messdaten = []
    for a, ind, ts, val in arr[1:]:
        t = datetime.fromtimestamp(ts)
        messdaten.append(Messdaten(wid, t, timedelta(0,60,0), 0, gu, gi, gp, wu, wi, val/100, 30))

    engine.execute("DELETE FROM messdaten;")    
    session = Session(bind=engine)
    print("created session")
    session.add_all(messdaten)
    session.commit()