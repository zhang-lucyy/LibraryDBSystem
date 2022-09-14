from src.swen344_db_utils import exec_commit, exec_get_all, exec_sql_file

def rebuild_tables():
    drop_sql = """
        DROP SCHEMA IF EXISTS library;
    """
    exec_commit(drop_sql)
    exec_sql_file('db-lz3744/src/library_schema.sql')
    exec_sql_file('db-lz3744/tests/test_library_schema.sql')

def get_all_users():
    users = exec_get_all('SELECT id, name FROM users ORDER BY id')
    return users

def main():
    rebuild_tables()

main()