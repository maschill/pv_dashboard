from sqlalchemy import create_engine


if __name__ == '__main__':
    #read db config from db_config.txt
    connection = None
    with open('pv_dashboard/src/db_config.txt', 'r') as fo:
        connection = fo.read().strip()
    engine = create_engine(connection)
    for row in engine.execute('SELECT Count(status) FROM messdaten'):
        print(row)