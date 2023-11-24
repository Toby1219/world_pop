import sqlite3


class SQlite:

    def __init__(self, name_db, table):
        self.cur = None
        self.conn = None
        self.table = table
        self.name_db = name_db
        self.connection()

    def connection(self):
        self.conn = sqlite3.connect(f'{self.name_db}')
        self.cur = self.conn.cursor()
        return self.cur

    def create_table(self, *args):
        assert args, "please enter a valid key word arguments(kwargs)"
        place_h = ', '.join([va for va in args])
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS {self.table} ({place_h})")
        return self.cur

    def insert_table(self, data: list, many=False):
        if many:
            for da in data:
                placeholders = ', '.join(['?' for _ in range(len(da))])
            self.cur.executemany(f"INSERT INTO {self.table} VALUES ({placeholders})", data)
            self.conn.commit()
            print(self.cur.rowcount, "data inserted.")
        else:
            placeholders = ', '.join(['?' for _ in range(len(data))])
            self.cur.execute(f"INSERT INTO {self.table} VALUES ({placeholders})", data)
            self.conn.commit()
            print(self.cur.rowcount, "data inserted.")
        return self.cur

    def update_(self, *args: str):
        assert args, "please enter a valid str(arguments)"
        pl = args[0]
        pl2 = args[1]
        pl3 = args[2]
        self.cur.execute(f"UPDATE {self.table} SET {pl} = '{pl2}' WHERE {pl} = '{pl3}'")
        self.conn.commit()
        return self.cur

    def view_all(self, *args, all_=False, limit=False, **kwargs):
        for i in kwargs.items():
            pass
        if all_:
            if limit:
                self.cur.execute(f"SELECT * FROM {self.table} LIMIT {i[1]}")
                x = self.cur.fetchall()
                for x in x:
                    print(x)
            else:
                self.cur.execute(f"SELECT * FROM {self.table}")
                x = self.cur.fetchall()
                for x in x:
                    print(x)

        else:
            assert args, "please enter a valid str(arguments) OR set all_=True"
            if limit:
                pl = ', '.join([i for i in args])
                self.cur.execute(f"SELECT {pl} FROM {self.table} LIMIT {i[1]}")
                x = self.cur.fetchall()
                for x in x:
                    print(x)
            else:
                pl = ', '.join([i for i in args])
                self.cur.execute(f"SELECT {pl} FROM {self.table}")
                x = self.cur.fetchall()
                for x in x:
                    print(x)
        return self.cur

    def delete_data(self, *args):
        assert args, "please enter a valid str(arguments) (TWO args ALLOWED)"
        pl = args[0]
        pl2 = args[1]
        self.cur.execute(f"DELETE FROM {self.table} WHERE {pl} = '{pl2}'")
        self.conn.commit()
        print(self.cur.rowcount, "record(s) deleted")
        return self.cur

    def drop_table(self):
        self.cur.execute(f"DROP TABLE IF EXISTS {self.table}")

