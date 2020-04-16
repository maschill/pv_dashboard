from sqlalchemy import Column, Integer, String, DateTime, Float, Interval, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Standort(Base):
    __tablename__= "standort"
    ort_id = Column(Integer, primary_key=True, autoincrement=False)
    ort_name = Column(String(50))

    def __init__(self,ort_id, ort_name):
        self.ort_id = ort_id
        self.ort_name = ort_name

class Betriebsart(Base):
    __tablename__= "betriebsart"

    status = Column(Integer, primary_key=True, autoincrement=False)
    short_desc = Column(String(50))
    long_desc = Column(String(500))

    def __init__(self,status, short_desc, long_desc):
        self.status = status
        self.short_desc = short_desc
        self.long_desc = long_desc

class Wechselrichter(Base):
    __tablename__= "wechselrichter"

    wechselrichter_id = Column(Integer, primary_key=True, autoincrement=False )
    ort_id = Column(Integer, ForeignKey("standort.ort_id"))
    max_leistung = Column(Float)

    def __init__(self, wechselrichter_id, ort, max_leistung):
        self.wechselrichter_id = wechselrichter_id
        self.ort_id = ort
        self.max_leistung = max_leistung


class Messdaten(Base):
    __tablename__= "messdaten"

    wechselrichter_id = Column(Integer, ForeignKey("wechselrichter.wechselrichter_id"), primary_key=True)
    uhrzeit = Column(DateTime(timezone=True), primary_key=True)
    betriebszeit = Column(Interval)
    status = Column(Integer, ForeignKey("betriebsart.status"))
    gleichstrom_spannung =  Column(Float)
    gleichstrom_strom =  Column(Float)
    gleichstrom_leistung = Column(Integer)
    wechselstrom_spannung =  Column(Float)
    wechselstrom_strom = Column(Float)
    wechselstrom_leistung = Column(Integer)
    temperatur_wechselrichter = Column(Integer)
    insert_timestamp = Column(DateTime(timezone=True))

    def __init__(self, 
                 wechselrichter_id,
                 uhrzeit,
                 betriebszeit,
                 status,
                 gleichstrom_spannung,
                 gleichstrom_strom,
                 gleichstrom_leistung,
                 wechselstrom_spannung,
                 wechselstrom_strom,
                 wechselstrom_leistung,
                 temperatur_wechselrichter,
                 insert_timestamp):
        self.wechselrichter_id = wechselrichter_id
        self.uhrzeit = uhrzeit
        self.betriebszeit = betriebszeit
        self.status = status
        self.gleichstrom_spannung = gleichstrom_spannung
        self.gleichstrom_strom = gleichstrom_strom
        self.gleichstrom_leistung = gleichstrom_leistung
        self.wechselstrom_spannung = wechselstrom_spannung
        self.wechselstrom_strom = wechselstrom_strom
        self.wechselstrom_leistung = wechselstrom_leistung
        self.temperatur_wechselrichter = temperatur_wechselrichter
        self.insert_timestamp = insert_timestamp
