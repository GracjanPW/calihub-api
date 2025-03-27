import psycopg
import os 

SUPERUSER_DB_CONFIG = {
    'dbname': 'postgres',
    'user':'postgres',
    'password':'devpassword',
    'host':'localhost',
    'port': 5432
}

DB_CONFIG = {
    'dbname': 'calihub_dev_db',
    'user':'app_user',
    'password':'devpassword',
    'host':'localhost',
    'port': 5432
}

DIR = os.path.dirname(os.path.abspath(__file__)) 
MIGRATIONS_DIR = os.path.abspath(os.path.join(DIR, '../sql/dev_migrations'))
DEV_RESET_SQL = '00_dev_only.sql'

def pexec(connection, file_path): 
    with open(file_path, 'r') as sql_file:
        sqls = sql_file.read()
        sql_commands = sqls.split(';')
        with connection.cursor() as cursor:
            for command in sql_commands:
                if command.strip() == '':
                    continue
                cursor.execute(command)
        
        connection.commit()

def reset_db():
    try:
        conn = psycopg.connect(**SUPERUSER_DB_CONFIG)
        conn.autocommit = True
        print('Superuser connect to db')

        pexec(conn, os.path.join(MIGRATIONS_DIR, DEV_RESET_SQL))
        
        conn.close()
        print('Database reset')
    except Exception as e:
        print(f"Problem reseting database: {e}")


def run_migrations():
    try:
        conn = psycopg.connect(**DB_CONFIG)
        conn.autocommit = True
        print('Appuser connect to db')

        for file in os.listdir(MIGRATIONS_DIR):
            if file.endswith('.sql') and file != DEV_RESET_SQL:
                pexec(conn, os.path.join(MIGRATIONS_DIR, file))
                print(f'Migration {file} executed')
        conn.close()
    except Exception as e:
        print(f"Problem running migrations: {e}")

if __name__ == '__main__':
    reset_db()
    run_migrations()