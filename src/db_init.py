from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from db_schemes import Standort, Betriebsart, Wechselrichter, Messdaten

Base = declarative_base()

if __name__ == "__main__":
    standorte = [
        Standort(0, "huehnerstall"),
        Standort(1, "heuhalle")
    ]

    wechselrichter = [
        Wechselrichter(0, 0,8000 ),
        Wechselrichter(1, 0,8000),
        Wechselrichter(2, 0,8000),
        Wechselrichter(3, 0,5000),
        Wechselrichter(4, 1, 25000),
        Wechselrichter(5, 1, 4000),
        Wechselrichter(6, 1, 4000),
        Wechselrichter(7, 1, 4000)
    ]

    betriebsart = [
    Betriebsart(0, "Wechselrichter hat sich gerade eingeschaltet", "Nur kurz nach erstem Einschalten am Morgen."),
    Betriebsart(1, "Warten auf Start Selbsttest ist abgeschlossen", "der Powador wechselt in wenigen Sekunden in den Einspeisebetrieb."),
    Betriebsart(2, "Warten auf Ausschalten", "Generatorspannung und -leistung ist zu gering. Zustand bevor in die Nachtabschaltung übergegangen wird."),
    Betriebsart(3, "Konstantspannungsregler", "Beim Einspeisebeginn wird kurzzeitig mit konstanter Generatorspannung eingespeist (80 % der gemessenen Leerlaufspannung"),
    Betriebsart(4, "MPP-Regler", "ständige Suchbewegung Bei geringer Einstrahlung wird mit suchendem MPP-Regler eingespeist."),
    Betriebsart(5, "MPP-Regler", "ohne Suchbewegung Bei hoher Einstrahlung wird für maximalen Ertrag mit stationärem MPP-Regler eingespeist."),
    Betriebsart(6, "Wartemodus vor Einspeisung", "Netz- und Solarspannung testen Der Wechselrichter hat die Einspeisung auf Grund zu geringer Leistung von den PV-Modulen (z. B. Dämmerung) beendet. Ist die Generatorspannung größer als die Einschaltschwelle (410 V), beginnt der Wechselrichter nach einer länderspezifi schen Wartezeit (Elektrofachkraft, Abschnitt 4, Technische Daten) erneut mit der Einspeisung."),
    Betriebsart(7, "Wartemodus vor Selbsttest", "Netz und Solarspannung testen Der Wechselrichter wartet bis die Generatorspannung größer als die Einschaltschwelle ist und beginnt dann nach einer länderspezifischen Wartezeit den Selbsttest der Relais (Elektrofachkraft, Abschnitt 4, Technische Daten)."),
    Betriebsart(8, "Selbsttest der Relais", "Überprüfung der Netzrelais vor Beginn der Einspeisung."),
    Betriebsart(10, "Übertemperaturabschaltung", "Bei Überhitzung des Wechselrichters (Kühlkörpertemperatur >85 °C) durch zu hohe Umgebungstemperatur und fehlende Luftzirkulation schaltet sich der Wechselrichter ab."),
    Betriebsart(11, "Leistungsbegrenzung", "Schutzfunktion des Wechselrichters, wenn zu viel Generatorleistung geliefert wird oder der Kühlkörper des Gerätes heißer als 75 °C ist."),
    Betriebsart(12, "Überlastabschaltung", "Schutzfunktion des Wechselrichters, wenn zu viel Generatorleistung geliefert wird."),
    Betriebsart(13, "Überspannungsabschaltung", "Schutzfunktion des Wechselrichters, wenn Netzspannung L1 zu hoch ist."),
    Betriebsart(14, "Netzstörung", "(3-phasige Überwachung) Schutzfunktion des Wechselrichters, wenn die Messwerte einer der drei Netzphasen außerhalb der zulässigen Toleranz sind. Ursachen für die Netzstörung sind: Unterspannung, Überspannung, Unterfrequenz, Überfrequenz, Außenleiterfehler."),
    Betriebsart(15, "Übergang zur Nachtabschaltung", "Wechselrichter schaltet vom Bereitschaftsbetrieb in die Nachtabschaltung."),
    Betriebsart(18, "RCD Typ B-Abschaltung", "Fehlerstrom ist zu hoch, der integrierte allstromsensitive Fehlerstromschutzschalter hat einen unzulässig hohen Ableitstrom nach PE registriert."),
    Betriebsart(19, "Isolationswiderstand zu gering", "Isolationswiderstand von PV-/PV+ nach PE <1,2 MOhm."),
    Betriebsart(30, "Störung Messwandler", "Die Strom- und Spannungsmessungen im Wechselrichter sind nicht plausibel."),
    Betriebsart(31, "Fehler RCD Typ B-Modul", "Im allstromsensitiven Fehlerstromschutzschalter ist ein Fehler aufgetreten."),
    Betriebsart(32, "Fehler Selbsttest", "Bei der Netzrelaisüberprüfung ist ein Fehler aufgetreten, ein Netzrelais funktioniert nicht korrekt."),
    Betriebsart(33, "Fehler DC-Einspeisung", "Die Gleichstromeinspeisung ins Netz war zu groß."),
    Betriebsart(34, "Fehler Kommunikation", "Es ist ein Fehler in der internen Datenübertragung aufgetreten."),
    ]

    #read db config from db_config.txt
    connection = None
    with open('db_config.txt', 'r') as fo:
        connection = fo.read().strip()
        
    engine = create_engine(connection)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("created tables")

    session = Session(bind=engine)
    print("created session")
    session.add_all(standorte)
    session.commit()
    print("committed standorte")

    session.add_all(betriebsart)
    session.commit()
    print("committed betriebsarten")

    session.add_all(wechselrichter)
    session.commit()
    print("committed wechselrichter")
