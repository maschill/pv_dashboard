from sqlalchemy import create_engine
from db_schemes import Messdaten
from datetime import timedelta, datetime
import numpy as np
from sqlalchemy.orm import Session


if __name__ == '__main__':
    #read db config from db_config.txt
    connection = None
    with open('pv_dashboard/src/db_config.txt', 'r') as fo:
        connection = fo.read().strip()
    engine = create_engine(connection)

    #fix some values
    wv = 300
    gv, gs, gp = 0,0,0
    
    production_f = np.poly1d([ 0.01108983, -0.3066665 ,  2.2466976 , -1.7647764 ,  0.2467437 ])
    wp = np.random.normal(0,1,14*60) + production_f(np.linspace(0,14,14*60)) 
     

    wechselrichter = {k:v for k,v in zip(range(8), [8000,8000,8000,5000,25000,4000,4000,4000])}
    uhrzeit = datetime(2019,4,8,0,0,0)
    messdaten = []
    for i in range(1440):
        t = uhrzeit+timedelta(0,60*i)
        if i < 6*60 or i > 20*60: 
            wpi = 0
        else: 
            wpi = int(wp[i-20*60]*1000)
        for wid, mpower in wechselrichter.items():
            ws = (wpi*(mpower/66000))/wv
            messdaten.append(Messdaten(wid, t, timedelta(0,60,0),0, gv, gs, gp, wv, ws, wpi, 30))


    engine.execute("DELETE FROM messdaten;")    
    session = Session(bind=engine)
    print("created session")
    session.add_all(messdaten)
    session.commit()