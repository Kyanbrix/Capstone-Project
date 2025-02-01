import psycopg2


class ConnectionPool:
    conn = ''

    def __init__(self):
        self.conn = psycopg2.connect(database='postgres',
                                     user='postgres',
                                     password='password',
                                     port=5432)

    def connect(self):
        return self.conn.cursor()

    def close(self):
        self.conn.close()
