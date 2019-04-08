from sqlalchemy import Column, Integer, String, DateTime, Float, Interval, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Standort(Base):
    tablename = "__standort__"
    ort_id = Column(Integer, primary_key=True)
    ort_name = Column(String(50))

class Betriebsart(Base):
    tablename = "__betriebsart__"

    status = Column(Integer, primary_key=True)
    short_desc = Column(String(50))
    long_desc = Column(String(250))

class Wechselrichter(Base):
    tablename = "__wechselrichter__"

    wechselrichter_id = Column(Integer, primary_key=True)
    ort = Column(String(50), ForeignKey("standort.ort_name"))
    max_leistung = Column(Float)


class Messdaten(Base):
    tablename = "__messdaten__"

    wechselrichter_id = Column(Integer, ForeignKey("wechselrichter.wechselrichter_id"), primary_key=True)
    uhrzeit = Column(DateTime, primary_key=True)
    betriebszeit = Column(Interval)
    status = Column(Integer, ForeignKey("betriebsart.status"))
    gleichstrom_spannung =  Column(Float)
    gleichstrom_strom =  Column(Float)
    gleichstrom_leistung = Column(Integer)
    wechselstrom_spannung =  Column(Float)
    wechselstrom_strom = Column(Float)
    wechselstrom_leistung = Column(Integer)
    temperatur_wechselrichter = Column(Integer)