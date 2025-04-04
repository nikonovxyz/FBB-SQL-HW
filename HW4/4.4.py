import sys
import psycopg2

class DBInsertDelete:
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
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f'Error connecting to database: ', e)
            self.conn = None
            self.cursor = None

    def show_table(self):
        try:
            self.cursor.execute(f'SELECT * FROM "aircrafts_data"')
            rows = self.cursor.fetchall()

            if rows:
                for row in rows:
                    print(row)
            else:
                print('[Empty]')
        except Exception as e:
            print('Error showing table: ', e)

    def insert_row(self):
        aircraft_code = input('Enter aircraft_code with character type: ')
        model = input('Enter model with jsonb type: ')
        aircraft_range = input('Enter range with integer type: ')
        model_json = '{"en": "' + model + '"}'

        col_names = 'aircraft_code, model, range'
        query = 'INSERT INTO aircrafts_data (aircraft_code, model, "range") VALUES (%s, %s, %s)'

        try:
            print('Table before:')
            self.show_table()
            self.cursor.execute(query, (aircraft_code, model_json, aircraft_range))
            print('Table after:')
            self.show_table()
            self.commit_prompt()
        except Exception as e:
            self.conn.rollback()
            print('Error during INSERT: ', e)

    def delete_row(self):
        condition = input('Enter condition for DELETE: ')

        if not condition.strip():
            print('No condition provided, DELETE aborted')
            return

        query = f'DELETE FROM Aircrafts WHERE {condition}'

        try:
            print('Table before:')
            self.show_table()
            self.cursor.execute(query)
            print('Table after:')
            self.show_table()
            self.commit_prompt()
        except Exception as e:
            self.conn.rollback()
            print('Error during DELETE: ', e)

    def commit_prompt(self):
        if input('Press 1 to rollback: ').strip() != '1':
            try:
                self.conn.commit()
                print('Your table is:')
                self.show_table()
            except Exception as e:
                print('Error committing transaction: ', e)
        else:
            try:
                self.conn.rollback()
                print('Your table is:')
                self.show_table()
            except Exception as e:
                print('Error rolling back transaction: ', e)

    def close_connection(self):
        if self.cursor:
            self.cursor.close()

        if self.conn:
            self.conn.close()

        print('\nProcess finished with exit code 0')
        sys.exit(0)

    def run(self):
        host = input('Enter host: ')
        password = input('Enter password: ')
        self.connect(host, password)

        if not self.conn:
            return

        while True:
            print('1 — Insert, 2 — Delete, 0 — Exit. ')
            choice = input('Enter your choice: ')
            if choice == '1':
                self.insert_row()
            elif choice == '2':
                self.delete_row()
            elif choice == '0':
                self.close_connection()
            else:
                print('Invalid choice')

if __name__ == '__main__':
    app = DBInsertDelete(dbname='demo', user='myuser')
    app.run()
