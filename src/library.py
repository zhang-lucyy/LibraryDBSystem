from src.swen344_db_utils import *

def rebuild_tables():
    drop_sql = """
        DROP SCHEMA IF EXISTS library CASCADE;
    """
    exec_commit(drop_sql)
    exec_sql_file('db-lz3744/src/library_schema.sql')

'''
Returns all of the users in the system.
'''
def get_all_users():
    return exec_get_all("SELECT id, name FROM users ORDER BY id ASC")

'''
Returns a user's id given their name.
Parameter: 
    name(str): A user's first and last name. 
'''
def get_user_id(name):
    return exec_get_one("SELECT id FROM users WHERE users.name = %(name)s", {'name': name})

'''
Returns a user's contact info given their user id.
Parameter:
    id(): A user id
'''
def get_user_contact_info(id):
    return exec_get_one("""
        SELECT contact_info FROM users INNER JOIN checkout 
        ON checkout.user_id = '%(id)s'""", {'id': id})

'''
Returns all the books currently checked out by a user.
Parameter:
    id(): A user id
'''
def get_user_books(id):
    return exec_get_all("""
        SELECT title, book_type, author, publish_date 
        FROM inventory INNER JOIN checkout ON inventory.book_id = checkout.book_id
        WHERE checkout.user_id = '%(id)s' ORDER BY title ASC""",{'id': id})

'''
Returns a list of all books checked out (sorted by author).
For each book, it says who checked it out and when; return date (or if not returned);
remaining copies.
'''
def get_checked_out_books():
    return exec_get_all("""
        SELECT inventory.title, users.name, checkout.check_out_date, inventory.copies FROM users
        INNER JOIN checkout ON checkout.user_id = users.id
        INNER JOIN inventory ON inventory.book_id = checkout.book_id
        ORDER BY inventory.author ASC
    """)

'''
Returns all of the nonfiction books in the inventory.
'''
def get_nonfiction_books():
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, inventory.copies 
        FROM inventory WHERE inventory.book_type = 'Non-fiction'
    """)

'''
Returns all of the fiction books in the inventory.
'''
def get_fiction_books():
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, inventory.copies 
        FROM inventory WHERE inventory.book_type = 'Fiction'
    """)

'''
Returns all the books in the inventory that are written by a particular author.
Parameter:
    author(str): Author's name.
'''
def search_by_author(author):
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, 
        inventory.publish_date, inventory.copies FROM inventory 
        WHERE inventory.author = %(author)s""", {'author': author})

'''
Returns all of the books in the inventory that match the given title.
Parameter:
    title(str): A book title.
'''
def search_by_title(title):
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, 
        inventory.publish_date, inventory.copies FROM inventory 
        WHERE inventory.title = %(title)s""", {'title': title})

'''
Returns the number of book copies left given the book id.
Parameter:
    book_id(): A book's id.
''' 
def get_book_copies(book_id):
    return exec_get_one("""
        SELECT inventory.copies FROM inventory WHERE inventory.book_id
        = %(book_id)s""", {'book_id': book_id})

'''
Returns the corresponding book id given the book title.
Parameter:
    title(str): A book title.
'''
def get_book_id(title):
    return exec_get_one("""
        SELECT inventory.book_id FROM inventory WHERE inventory.title
        = %(title)s""", {'title': title})

'''
Creates a new account with the given name and contact info.
Parameters:
    name(str): The user's first and last name.
    contact_info(str): The user's email.
'''
def create_account(name, contact_info):
    return exec_commit("""
        INSERT INTO users (name, contact_info) VALUES (%(name)s, %(contact_info)s)
        """, {'name': name, 'contact_info': contact_info})

'''
Deletes a user's account given their name.
Parameter:
    name(str): The user's first and last name.
'''
def delete_account(name):
    return exec_commit("""
        DELETE FROM users WHERE users.name = %(name)s""", {'name': name})

'''

'''
def checkout_book(book_id, user_id, check_out_date):
    exec_commit("""
        UPDATE inventory SET copies = (copies - 1)
        WHERE book_id = %(book_id)s""", {'book_id': book_id})

    return exec_commit("""
        INSERT INTO checkout (book_id, user_id, check_out_date)
        VALUES (%(book_id)s, %(user_id)s, %(check_out_date)s)""",
        {'book_id': book_id, 'user_id': user_id, 'check_out_date': check_out_date})

def return_book(book_id, user_id, return_date):
    exec_commit("""
        UPDATE inventory SET copies = (copies + 1)
        WHERE book_id = %(book_id)s""", {'book_id': book_id})
    
    return exec_commit("""
        UPDATE checkout SET return_date = %(return_date)s
        WHERE book_id = %(book_id)s
        AND user_id = %(user_id)s""",
        {'return_date': return_date, 'book_id': book_id, 'user_id': user_id})

def reserve_book(reserve_book_id, user_id):
    book_copies = get_book_copies(reserve_book_id)
    if (book_copies[0] == 0):
        return exec_commit("""
            INSERT INTO reserve(reserve_book_id, user_id)
            VALUES (%(reserve_book_id)s, %(user_id)s)""",
            {'reserve_book_id': reserve_book_id, 'user_id': user_id})
    else:
        raise Exception("copies of the book are still available")


def main():
    rebuild_tables()

main()