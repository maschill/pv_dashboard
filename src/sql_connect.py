from sqlalchemy import create_engine


if __name__ == '__main__':
    #read db config from db_config.txt
    connection = None
    with open('src/db_config.txt', 'r') as fo:
        connection = fo.read().strip()
    engine = create_engine(connection)
    query = 'SELECT uhrzeit, wechselrichter_id, wechselstrom_leistung FROM messdaten WHERE wechselstrom_leistung > 100 ORDER BY uhrzeit;'
    # query = 'SELECT min(uhrzeit), wechselstrom_leistung FROM messdaten WHERE wechselstrom_leistung > 5000 '
    query = 'SELECT uhrzeit, wechselrichter_id, MAX(wechselstrom_leistung) FROM messdaten GROUP BY wechselrichter_id'
    for row in engine.execute(query):
        print(row)
