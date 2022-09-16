from swen344_db_utils import *

def rebuild_tables():
    drop_sql = """
        DROP SCHEMA IF EXISTS library CASCADE;
    """
    exec_commit(drop_sql)
    exec_sql_file('db-lz3744/src/library_schema.sql')
    exec_sql_file('db-lz3744/tests/test_library_schema.sql')

def get_all_users():
    return exec_get_all("SELECT id, name FROM users ORDER BY id ASC")

def get_user_contact_info(id):
    return exec_get_one("""
        SELECT contact_info FROM users INNER JOIN checkout 
        ON checkout.user_id = '%(id)s'""", {'id': id})

def get_user_books(id):
    return exec_get_all("""
        SELECT title, book_type, author, publish_date 
        FROM inventory INNER JOIN checkout ON inventory.book_id = checkout.checked_out 
        WHERE checkout.user_id = '%(id)s' ORDER BY title ASC""",{'id': id})

def get_checked_out_books():
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author FROM users
        INNER JOIN checkout ON checkout.user_id = users.id
        INNER JOIN inventory ON inventory.book_id = checkout.checked_out
        ORDER BY users.name ASC
    """)

def get_nonfiction_books():
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, inventory.copies 
        FROM inventory WHERE inventory.book_type = 'Non-fiction'
    """)

def get_fiction_books():
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, inventory.copies 
        FROM inventory WHERE inventory.book_type = 'Fiction'
    """)

def search_by_author(author):
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, 
        inventory.publish_date, inventory.copies FROM inventory 
        WHERE inventory.author = %(author)s""", {'author': author})

def main():
    rebuild_tables()

main()