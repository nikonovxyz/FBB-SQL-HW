import sys
from sqlalchemy import *
from sqlalchemy.orm import Session, sessionmaker, declarative_base


Base = declarative_base()

class Aircraft(Base):
    __tablename__ = 'aircrafts_data'
    aircraft_code = Column(String, primary_key=True)
    model = Column(JSON)
    range = Column(Integer)

    def __repr__(self):
        return f'<aircrafts_data(aircraft_code={self.aircraft_code}, model={self.model}, \
            range={self.range})>'

class DBORMInsertDelete:
    def __init__(self, dbname, user):
        self.dbname = dbname
        self.user = user
        self.engine = None
        self.session = None

    def connect(self, host, password):
        try:
            dsn = f'postgresql://{self.user}:{password}@{host}/{self.dbname}'
            self.engine = create_engine(dsn)
            self.session = Session(bind=self.engine)
        except Exception as e:
            print(f'Error connecting to database: {e}')
            self.session = None

    def show_table(self):
        try:
            rows = self.session.query(Aircraft).all()
            if rows:
                for row in rows:
                    print(f"<aircrafts_data(aircraft_code={row.aircraft_code}, model={row.model}, range={row.range})>")
            else:
                print('[Empty]')
        except Exception as e:
            print('Error showing table: ', e)

    def insert_row(self):
        aircraft_code = input('Enter aircraft_code with character type: ').strip()
        model = input('Enter model with json type: ').strip()
        aircraft_range = int(input('Enter range with integer type: ').strip())
        new_aircraft = Aircraft(
            aircraft_code=aircraft_code,
            model={"en": model},
            range=aircraft_range
        )

        try:
            print('Table before:')
            self.show_table()
            self.session.add(new_aircraft)
            print('Table after:')
            self.show_table()
            self.commit_prompt()
        except Exception as e:
            self.session.rollback()
            print('Error during INSERT: ', e)

    def delete_row(self):
        condition = input('Enter condition for DELETE: ').strip()

        if not condition:
            print('No condition provided, DELETE aborted')
            return

        try:
            print('Table before:')
            self.show_table()

            deleted_rows = self.session.query(Aircraft).filter(text(condition)).all()
            for row in deleted_rows:
                self.session.delete(row)

            print('Table after:')
            self.show_table()
            self.commit_prompt()
        except Exception as e:
            self.session.rollback()
            print('Error during DELETE: ', e)

    def commit_prompt(self):
        if input('Press 1 to rollback: ').strip() != '1':
            try:
                self.session.commit()
                print('Your table is:')
                self.show_table()
            except Exception as e:
                print('Error committing transaction: ', e)
        else:
            try:
                self.session.rollback()
                print('Your table is:')
                self.show_table()
            except Exception as e:
                print('Error rolling back transaction: ', e)

    def close_connection(self):
        if self.session:
            self.session.close()

        print('\nProcess finished with exit code 0')
        sys.exit(0)

    def run(self):
        host = input('Enter host: ').strip()
        password = input('Enter password: ').strip()
        self.connect(host, password)

        if not self.session:
            return

        while True:
            print('1 – Insert, 2 – Delete, 0 – Exit. ')
            choice = input('Enter your choice: ').strip()
            if choice == '1':
                self.insert_row()
            elif choice == '2':
                self.delete_row()
            elif choice == '0':
                self.close_connection()
            else:
                print('Invalid choice')

if __name__ == '__main__':
    app = DBORMInsertDelete(dbname='demo', user='myuser')
    app.run()
