import csv
from datetime import datetime
from src.swen344_db_utils import *

def rebuild_tables():
    drop_sql = """
        DROP SCHEMA IF EXISTS library CASCADE;
    """
    exec_commit(drop_sql)
    exec_sql_file('db-lz3744/src/library_schema.sql')

'''
Returns all of the users in the system.
Returns:
    (list): A list of users (tuples)
'''
def get_all_users():
    return exec_get_all("SELECT id, name FROM users ORDER BY id ASC")

'''
Returns a user's id given their name.
Parameter: 
    name(str): A user's first and last name. 
Returns:
    (int): A user's id number in the system.
'''
def get_user_id(name):
    return exec_get_one("SELECT id FROM users WHERE users.name = %(name)s", {'name': name})[0]

'''
Returns a user's contact info given their user id.
Parameter:
    id(int): A user id.
Returns:
    (str): A user's contact info.
'''
def get_user_contact_info(id):
    return exec_get_one("""
        SELECT contact_info FROM users INNER JOIN checkout 
        ON checkout.user_id = '%(id)s'""", {'id': id})

'''
Returns all of the books in inventory.
Returns:
    (list): A list of books (tuples).
'''
def get_all_books():
    return exec_get_all("""
        SELECT * FROM inventory
    """)

'''
Returns all the books currently checked out by a user.
Parameter:
    id(int): A user id.
Returns:
    (list): A list of books (tuples).
'''
def get_user_books(id):
    return exec_get_all("""
        SELECT title, book_type, author, publish_date 
        FROM inventory INNER JOIN checkout ON inventory.book_id = checkout.book_id
        WHERE checkout.user_id = '%(id)s' ORDER BY title ASC""",{'id': id})

'''
Returns all books checked out (sorted by book type / author).
For each book, it says who checked it out and when; return date (or if not returned);
remaining copies.
Returns:
    (list): A list of books (tuples).
'''
def get_checked_out_books():
    return exec_get_all("""
        SELECT inventory.title, users.name, checkout.check_out_date, checkout.return_date,
        inventory.copies FROM users
        INNER JOIN checkout ON checkout.user_id = users.id
        INNER JOIN inventory ON inventory.book_id = checkout.book_id
        ORDER BY inventory.book_type, inventory.author ASC
    """)

'''
Returns all of the nonfiction books in the inventory.
Returns:
    (list): A list of books (tuples).
'''
def get_nonfiction_books():
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, inventory.copies 
        FROM inventory WHERE inventory.book_type = 'Non-fiction'
    """)

'''
Returns all of the fiction books in the inventory.
Returns:
    (list): A list of books (tuples).
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
Returns:
    (list): A list of books (tuples).
'''
def search_by_author(author):
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, 
        inventory.publish_date, inventory.copies FROM inventory 
        WHERE inventory.author = %(author)s""", {'author': author})[0]

'''
Returns all of the books in the inventory that match the given title.
Parameter:
    title(str): A book title.
Returns:
    (list): A list of books (tuples).
'''
def search_by_title(title):
    return exec_get_all("""
        SELECT inventory.title, inventory.book_type, inventory.author, 
        inventory.publish_date, inventory.copies FROM inventory 
        WHERE inventory.title = %(title)s""", {'title': title})

'''
Returns the number of book copies at the specified library given
the library id and book id.
Parameter:
    library_id(int): A library id.
    book_id(int): A book's id.
Returns:
    (int): Number of book copies.
''' 
def get_book_copies(library_id, book_id):
    return exec_get_one("""
        SELECT book_copies FROM library_stock 
        WHERE library_stock.library_id = %(library_id)s
        AND library_stock.book_id = %(book_id)s""",
        {'library_id': library_id, 'book_id': book_id})

'''
Returns the corresponding book id given the book title.
Parameter:
    title(str): A book title.
Returns:
    (int): A book's id.
'''
def get_book_id(title):
    return exec_get_one("""
        SELECT inventory.book_id FROM inventory WHERE inventory.title
        = %(title)s""", {'title': title})[0]

'''
Creates a new account with the given name and contact info.
Parameters:
    name(str): The user's first and last name.
    contact_info(str): The user's email.
'''
def create_account(name, contact_info):
    exec_commit("""
        INSERT INTO users (name, contact_info) VALUES (%(name)s, %(contact_info)s)
        """, {'name': name, 'contact_info': contact_info})

'''
Deletes a user's account given their name.
Parameter:
    name(str): The user's first and last name.
'''
def delete_account(name):
    exec_commit("""
        DELETE FROM users WHERE users.name = %(name)s""", {'name': name})

'''
When books are checked out, they have a pre-assigned maximum lending
time of 2 weeks.
Parameter:
    user_id(int): A user id.
    book_id(int): A book id.
'''
def add_due_date(user_id, book_id):
    exec_commit("""
        UPDATE checkout
        SET due_date = check_out_date +  interval '2 weeks'
        WHERE user_id = %(user_id)s
        AND book_id = %(book_id)s""",
        {'user_id': user_id, 'book_id': book_id})

'''
User checks out a book at a given library. If a user is overdue on a book,
no further checkouts will be allowed.
Parameter:
    library_id(int): A library id.
    book_id(int): A book id.
    user_id(int): A user id.
    check_out_date(date): The date the book is checked out.
'''
def checkout_book(library_id, book_id, user_id, check_out_date):
    # check if there's any overdue books, if there are, user cannot make further checkouts
    due_dates = exec_get_all("""
        SELECT due_date FROM checkout
        WHERE user_id = %(user_id)s
        AND due_date IS NOT NULL""",
        {'user_id': user_id})

    overdue = 0
    for dates in due_dates:
        if (datetime.strptime(check_out_date, '%Y-%m-%d').date() > dates[0]):
            overdue += 1
            break
    
    if (overdue == 1):
        raise Exception("Cannot checkout book because user has an overdue book")

    else:
        # updates master inventory
        exec_commit("""
            UPDATE inventory SET copies = (copies - 1)
            WHERE book_id = %(book_id)s""", {'book_id': book_id})

        # updates library inventory
        exec_commit("""
            UPDATE library_stock SET book_copies = (book_copies - 1)
            WHERE book_id = %(book_id)s
            AND library_stock.library_id = %(library_id)s""",
            {'book_id': book_id, 'library_id': library_id})

        exec_commit("""
            INSERT INTO checkout (library_id, book_id, user_id, check_out_date)
            VALUES (%(library_id)s, %(book_id)s, %(user_id)s, %(check_out_date)s)""",
            {'library_id': library_id, 'book_id': book_id, 'user_id': user_id, 'check_out_date': check_out_date})

        add_due_date(user_id, book_id)

'''
User returns a book at a given library.
Parameter:
    library_id(int): A library id.
    book_id(int): A book id.
    user_id(int): A user id.
    return_date(date): The date the book is returned.
'''
def return_book(library_id, book_id, user_id, return_date):
    # updates master inventory
    exec_commit("""
        UPDATE inventory SET copies = (copies + 1)
        WHERE book_id = %(book_id)s""", {'book_id': book_id})

    # updates library inventory
    exec_commit("""
        UPDATE library_stock SET book_copies = (book_copies + 1)
        WHERE book_id = %(book_id)s
        AND library_stock.library_id = %(library_id)s""",
        {'book_id': book_id, 'library_id': library_id})
    
    # updates table to show return date & sets previous due date to null
    exec_commit("""
        UPDATE checkout SET return_date = %(return_date)s,
        due_date = NULL
        WHERE book_id = %(book_id)s
        AND user_id = %(user_id)s
        AND checkout.library_id = %(library_id)s""",
        {'return_date': return_date, 'book_id': book_id, 'user_id': user_id, 'library_id': library_id})

'''
User reserves a book, only reserves successfully if there are no copies
of the book left at the specified library.
Parameters:
    library_id(int): A library id.
    reserve_book_id(int): A book id.
    user_id(int): A user id.
'''
def reserve_book(library_id, reserve_book_id, user_id):
    book_copies = get_book_copies(library_id, reserve_book_id)
    if (book_copies[0] == 0):
        exec_commit("""
            INSERT INTO reserve(library_id, reserve_book_id, user_id)
            VALUES (%(library_id)s, %(reserve_book_id)s, %(user_id)s)""",
            {'library_id': library_id, 'reserve_book_id': reserve_book_id, 'user_id': user_id})
    else:
        raise Exception("copies of the book are still available")

'''
Loads the set of information on books from a file and adds it to the database.
Parameter:
    filename(str): Csv file with test data.
'''
def insert_data_from_csv(filename):
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)

        for record in csv_reader:
            title = record[0]
            author = record[1]
            summary = record[2]
            book_type = record[3]
            copies = record[5]

            exec_commit("""
                INSERT INTO inventory(title, book_type, author, publish_date, summary, copies)
                VALUES (%(title)s, %(book_type)s, %(author)s, NULL, %(summary)s, %(copies)s)""",
                {'title': title, 'book_type': book_type, 'author': author, 'summary': summary, 'copies': copies})

'''
Adds a new book to the master inventory.
Parameters:
    title(str): Title of a book.
    book_type(str): Genre of a book.
    author(str): Author's name.
    copies(int): Number of copies of the book.
'''
def add_new_book(title, book_type, author, copies):
    exec_commit("""
        INSERT INTO inventory(title, book_type, author, copies)
        VALUES (%(title)s, %(book_type)s, %(author)s, %(copies)s)""",
        {'title': title, 'book_type': book_type, 'author': author, 'copies': copies})

'''
Adds a new book to the specified library's inventory.
Parameters:
    library_id(int): A library's id.
    book_id(int): A book's id.
    book_copies(int): Number of copies of the book.
'''
def add_to_library(library_id, book_id, book_copies):
    exec_commit("""
        INSERT INTO library_stock(library_id, book_id, book_copies)
        VALUES (%(library_id)s, %(book_id)s, %(book_copies)s)""",
        {'library_id': library_id, 'book_id': book_id, 'book_copies': book_copies})

'''
Returns a listing of a user's lending history including their late history.
Parameter:
    user_id(int): A user id.
Returns:
    (list): A list of the user's lending history.
'''
def get_user_history(user_id):
    return exec_get_all("""
        SELECT inventory.title, check_out_date, due_date, return_date
        FROM checkout
        INNER JOIN inventory ON inventory.book_id = checkout.book_id
        WHERE user_id = %(user_id)s""",
        {'user_id': user_id})

'''
As a librarian, this returns a comprehensive list of all late books and histories
at the specified library.
Parameter:
    library_id(int): A library's id.
Returns:
    (list): All checkout histories including late books.
'''
def get_all_histories(library_id):
    #NEEDS TESTING
    return exec_get_all("""
        SELECT inventory.title, check_out_date, due_date, return_date
        FROM checkout
        INNER JOIN inventory ON inventory.book_id = checkout.book_id
        WHERE library_id = %(library_id)s""",
        {'library_id': library_id})

'''
Runs a report listing all books in all libraries, organized by library location
and book title with the count of books at each location.
Returns:
    (list): A list of all books in all libraries (tuples).
'''
def report_on_all_libraries():
    #NEEDS TESTING
    return exec_get_all("""
        SELECT libraries.library_name, inventory.title, book_copies
        FROM library_stock
        INNER JOIN inventory ON inventory.book_id = library_stock.book_id
        INNER JOIN libraries ON libraries.library_id = library_stock.library_id
        ORDER BY libraries.library_name, inventory.title ASC
    """)

def main():
    rebuild_tables()

main()