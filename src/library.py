from src.swen344_db_utils import *

def rebuild_tables():
    drop_sql = """
        DROP SCHEMA IF EXISTS library CASCADE;
    """
    exec_commit(drop_sql)
    exec_sql_file('db-lz3744/src/library_schema.sql')

def get_all_users():
    return exec_get_all("SELECT id, name FROM users ORDER BY id ASC")

def get_user_id(name):
    return exec_get_one("SELECT id FROM users WHERE users.name = %(name)s", {'name': name})

def get_user_contact_info(id):
    return exec_get_one("""
        SELECT contact_info FROM users INNER JOIN checkout 
        ON checkout.user_id = '%(id)s'""", {'id': id})

def get_user_books(id):
    return exec_get_all("""
        SELECT title, book_type, author, publish_date 
        FROM inventory INNER JOIN checkout ON inventory.book_id = checkout.book_id
        WHERE checkout.user_id = '%(id)s' ORDER BY title ASC""",{'id': id})

def get_checked_out_books():
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author FROM users
        INNER JOIN checkout ON checkout.user_id = users.id
        INNER JOIN inventory ON inventory.book_id = checkout.book_id
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

def search_by_title(title):
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, 
        inventory.publish_date, inventory.copies FROM inventory 
        WHERE inventory.title = %(title)s""", {'title': title})
    
def get_book_copies(book_id):
    return exec_get_one("""
        SELECT inventory.copies FROM inventory WHERE inventory.book_id
        = %(book_id)s""", {'book_id': book_id})

def get_check_out_date(book_id):
    return exec_get_one("""
        SELECT check_out_date FROM checkout WHERE checkout.book_id
        = %(book_id)s AND 
    """)

def create_account(name, contact_info):
    return exec_commit("""
        INSERT INTO users (name, contact_info) VALUES (%(name)s, %(contact_info)s)
        """, {'name': name, 'contact_info': contact_info})

def delete_account(name):
    user_id = get_user_id(name)
    exec_commit("""
        DELETE FROM return WHERE return.user_id = %(user_id)s""", {'user_id': user_id})

    return exec_commit("""
        DELETE FROM users WHERE users.name = %(name)s""", {'name': name})

def checkout_book(book_id, user_id, check_out_date):
    exec_commit("""
        UPDATE inventory SET copies = (copies - 1)
        WHERE book_id = %(book_id)s""", {'book_id': book_id})

    return exec_commit("""
        INSERT INTO checkout (book_id, user_id, check_out_date)
        VALUES (%(book_id)s, %(user_id)s, %(check_out_date)s)""",
        {'book_id': book_id, 'user_id': user_id, 'check_out_date': check_out_date})

def return_book(book_id, user_id, date_returned):
    exec_commit("""
        UPDATE inventory SET copies = (copies + 1)
        WHERE book_id = %(book_id)s""", {'book_id': book_id})

    checked_out_date = get_check_out_date(book_id)
    
    book = exec_commit("""
        INSERT INTO return (book_id, user_id, check_out_date, return_date) 
        VALUES (%(book_id)s, %(user_id)s, %(checked_out_date)s, %(date_returned)s)""", 
        {'book_id': book_id, 'user_id': user_id, 'checked_out_date': checked_out_date,'date_returned': date_returned})

    exec_commit("""
        DELETE FROM checkout WHERE checkout.book_id = %(book_id)s""", {'book_id': book_id})

    return book;

def reserve_book(book_id, user_id):
    book_copies = get_book_copies(book_id)
    if (book_copies == 0):
        return exec_commit("""
            INSERT INTO reserve(reserve_book_id, user_id)
            VALUES (%(book_id)s, %(user_id)s)""",
            {'reserve_book_id': book_id, 'user_id': user_id})
    else:
        raise Exception("copies of the book are still available")

def main():
    rebuild_tables()

main()