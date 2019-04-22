from sqlalchemy import create_engine


if __name__ == '__main__':
    #read db config from db_config.txt
    connection = None
    with open('src/db_config.txt', 'r') as fo:
        connection = fo.read().strip()
    engine = create_engine(connection)
    for row in engine.execute('SELECT * FROM wechselrichter;'): 
        print(row)
