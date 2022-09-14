from src.swen344_db_utils import *

def rebuild_tables():
    drop_sql = """
        DROP SCHEMA IF EXISTS library CASCADE;
    """
    exec_commit(drop_sql)
    exec_sql_file('db-lz3744/src/library_schema.sql')
    exec_sql_file('db-lz3744/tests/test_library_schema.sql')

def get_all_users():
    return exec_get_all('SELECT id, name FROM users ORDER BY id ASC')

#def get_user_books(id):
    #return exec_get_one("SELECT * FROM inventory INNER JOIN checkout ON inventory.book_id = checkout.checked_out WHERE (checkout.user_id = %s)", (id))

# need to rewrite these two test functions to take user id as parameter
def get_art_user_books():
    return exec_get_one("SELECT * FROM inventory INNER JOIN checkout ON inventory.book_id = checkout.checked_out WHERE checkout.user_id = 4")

def get_gleason_user_books():
    return exec_get_one("SELECT title FROM inventory INNER JOIN checkout ON inventory.book_id = checkout.checked_out WHERE checkout.user_id = 3")

def main():
    rebuild_tables()

main()