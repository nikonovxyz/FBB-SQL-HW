import sys
import psycopg2

class DBConditionalSelectTable:
    def __init__(self, dbname, user):
        self.dbname = dbname
        self.user = user
        self.conn = None
        self.cursor = None

    def connect(self, host, password):
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=password,
                host=host,
                connect_timeout=5
                # Я сначала путался с адресом, и программа висела,
                # если адрес был неправильный, поэтому я добавил таймаут
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
        # Exception — это плохо, но я не знаю, что конкретно может пойти не так
            print(f'Error connecting to database:', e)
            self.conn = None
            self.cursor = None

    def get_table_list(self):
        if not self.cursor:
            print('No database connection')
            return []
        try:
            self.cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                """
            )

            table_names =  self.cursor.fetchall()
            if not table_names:
                print(f'No tables in database {self.dbname}')
                return []

            return [row[0] for row in table_names]
        except Exception as e:
            print('Error retrieving table list:', e)
            return []

    def query_table(self, table_name, condition):
        if not self.cursor:
            print('No database connection')
            return []

        query = f'SELECT * FROM {table_name}'

        if condition.strip():
            query += f' WHERE {condition}'

        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print('Error executing query:', e)
            return []

    def close_connection(self):
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()

        print('\nProcess finished with exit code 0')
        sys.exit(0)

    def run(self):
        host = input('Enter your host address: ')
        password = input('Enter your password: ')

        self.connect(host, password)
        if not self.conn:
            return

        tables = self.get_table_list()
        if not tables:
            self.close_connection()
            return

        print('\nSelect table number you want:')

        for i, t in enumerate(tables, start=1):
            print(f'{i} {t}')

        try:
            table_num = int(input())
            table_index = table_num - 1

            if table_index < 0 or table_index >= len(tables):
                print('Invalid table number')
                self.close_connection()
                return
        except ValueError:
            print('Invalid input')
            self.close_connection()
            return

        table_name = tables[table_index]
        condition = input('Enter condition if you want: ')
        rows = self.query_table(table_name, condition)

        for row in rows:
            print(row)

        self.close_connection()


if __name__ == '__main__':
    app = ConditionalSelect(dbname='demo', user='myuser')
    app.run()

