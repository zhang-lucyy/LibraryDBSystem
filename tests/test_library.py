from datetime import date, datetime
import unittest
from src.swen344_db_utils import *
from src.library import *

class TestLibrary(unittest.TestCase):
    
    def set_up():
        rebuild_tables()

    def test_verify_users_rows(self):
        expected = 4
        actual = get_all_users().__len__()
        
        self.assertEqual(expected, actual, 'incorrect count of rows for users table')
        print('\nNumber of rows in users table:', actual)

    def test_verify_inventory_rows(self):
        expected = 22
        actual = get_nonfiction_books().__len__() + get_fiction_books().__len__()
        
        self.assertEqual(expected, actual, 'incorrect count of rows for inventory table')
        print('\nNumber of rows in inventory table:', actual)

    def test_verify_library_rows(self):
        expected = 4
        actual = exec_get_all("""
            SELECT * FROM libraries
        """)
        
        self.assertEqual(expected, actual.__len__(), 'not all libraries are listed')
        print('\nLibraries:', actual)

    def test_verify_checkout_rows(self):
        expected = 5
        actual = get_checked_out_books().__len__()
        
        self.assertEqual(expected, actual, 'incorrect count of rows for checkout table')
        print('\nNumber of rows in checkout table:', actual)

    def test_get_user_contact_info(self):
        expected = 'ALovelace@gmail.com'
        actual = get_user_contact_info(1)[0];
        
        self.assertEqual(expected, actual, "Ada Lovelace's contact info is incorrect")
        print("\nAda Lovelace's contact info:", actual)

    def test_get_user_books_art(self):
        rebuild_tables()
        expected = []
        actual = get_user_books(4)
        
        self.assertEqual(expected, actual, 'expected empty list from Art')
        print("\nArt's checked out books:", actual)

    def test_get_user_books_gleason(self):
        expected = 2
        actual = get_user_books(3)
        
        self.assertEqual(expected, actual.__len__(), 'expected books The Lightning Thief and To Kill a Mockingbird are checked out by Gleason')
        print("\nJackie Gleason's checked out books in alphabetical order:", actual)

    def test_get_nonfiction_books(self):
        expected = 4
        actual = get_nonfiction_books()
        
        self.assertEqual(expected, actual.__len__(), 'not all expected non-fiction books are listed')
        print('\nAll non-fiction books:', actual)

    def test_get_fiction_books(self):
        expected = 7
        actual = get_fiction_books()
        
        self.assertEqual(expected, actual.__len__(), 'not all expected fiction books are listed')
        print('\nAll fiction books:', actual)

    def test_search_by_author(self):
        expected = ('To Kill a Mockingbird', 'Fiction', 'Harper Lee', 1960, 1)
        actual = search_by_author('Harper Lee')
        
        self.assertEqual(expected, actual, 'not all books by Harper Lee are listed')
        print('\nBooks in inventory by Harper Lee:', actual)

    def test_create_account(self):
        create_account('Christopher Marlowe', 'CMarlowe@gmail.com')
        expected1 = [(5, 'Christopher Marlowe', 'CMarlowe@gmail.com')]
        actual1 = exec_get_all("""
            SELECT * FROM users WHERE name = \'Christopher Marlowe\'
        """)

        create_account('Francis Bacon', 'FBacon@gmail.com')
        expected2 = [(6, 'Francis Bacon', 'FBacon@gmail.com')]
        actual2 = exec_get_all("""
            SELECT * FROM users WHERE name = \'Francis Bacon\'
        """)

        self.assertEqual(expected1, actual1, 'did not create an account for Christopher Marlowe')
        self.assertEqual(expected2, actual2, 'did not create an account for Francis Bacon')
        print('\nChristopher Marlowe and Francis Bacon each sign up for a new account')

    def test_reserve_book_fail(self):
        user_id = get_user_id('Jackie Gleason')
        book_id = get_book_id('Figuring')

        with self.assertRaises(Exception) as cannot_reserve:
            reserve_book(1, book_id, user_id)
            self.assertTrue('Copies are still available' in cannot_reserve.exception)
        print('\nJackie Gleason reserves a book incorrectly')

    def test_reserve_book_success(self):
        user_id = get_user_id('Jackie Gleason')
        book_id = get_book_id('The Lord of the Rings')
        reserve_book(1, book_id, user_id)

        expected = [(1, 6, 3)]
        actual = exec_get_all("""
            SELECT * FROM reserve WHERE user_id = %(user_id)s""",
            {'user_id': user_id})

        self.assertEqual(expected, actual, 'did not successfully reserve a book')
        print('\nJackie Gleason successfully reserves a book')

    def test_return_book(self):
        user_id = get_user_id('Art Garfunkel')
        book_id = get_book_id('Frankenstein')
        checkout_book(1, book_id, user_id, '2020-09-10')

        expected = (1, 9, 4, date(2020, 9, 10), None, date(2020, 9, 13), 0.0)
        actual = return_book(1, book_id, user_id, '2020-09-13')

        self.assertEqual(expected, actual, 'Art did not return the book')
        print('\nArt Garfunkel returns a copy of “Frankenstein” three days after he borrowed it')

    def test_delete_account(self):
        #return_book(3, 3, 2, '2020-09-10')
        delete_account('Mary Shelley')

        expected = []
        actual = exec_get_all("""
            SELECT * FROM users WHERE name = 'Mary Shelley'
        """)

        self.assertEqual(expected, search_by_title('The Last Man'))
        self.assertEqual(expected, actual, "Mary Shelley's account should be deleted")
        print('\nMary Shelley deletes her account after finding no copies of "The Last Man" in the library')

    def test_insert_data_from_csv(self):
        insert_data_from_csv('src/Library.csv')
        expected = 29   # 20 from csv + 9 from schema insert
        actual = get_all_books().__len__()

        self.assertEqual(expected, actual, 'something wrong about book data')
        print('\nAll .csv books loaded successfully into database')

    def test_checkout_has_due_date(self):
        user_id = 2
        book_id = 1

        expected = (3, 1, 2, date(2020, 9, 10), date(2020, 9, 24), None, 0.0)
        actual = checkout_book(3, book_id, user_id, '2020-09-10')

        self.assertEqual(expected, actual, 'Pre-assigned due date is not correct')
        print('\nCheckout works correctly, book has pre-assigned due date')

    # test case sketches db3
    def test_fairport_checkouts(self):
        library_id = 2

        # Mary's account was previously deleted in db2 test case, so create a new one
        create_account('Mary Shelley', 'MShelley@gmail.com')
        # Mary checks out
        user_id = get_user_id('Mary Shelley')
        book_id = get_book_id('The Winds of Winter')
        checkout_book(library_id, book_id, user_id, '2022-01-02')

        expected = (2, book_id, user_id, date(2022, 1, 2), None, date(2022, 1, 10), 0.0)
        actual = return_book(library_id, book_id, user_id, '2022-01-10')

        self.assertEqual(expected, actual, 'Mary should have checked out on Jan. 2nd')
        print('\nMary checks out "The Winds of Winter" on Jan. 2nd and returns it in 8 days')


        # Ada checks out
        user_id = get_user_id('Ada Lovelace')
        book_id = get_book_id('The Winds of Winter')
        checkout_book(library_id, book_id, user_id, '2022-01-13')

        # tries to check out another book 15 days after
        with self.assertRaises(Exception) as cannot_checkout:
            checkout_book(library_id, get_book_id('The Lightning Thief'), user_id, '2022-01-28')
            self.assertTrue('User has a overdue book - no further checkouts will be allowed' in cannot_checkout.exception)
        self.assertEqual(2, get_user_history(user_id).__len__(), 'Ada should only have 2 books in his history')
        print('\nAda tries to check out another book 15 days after checking out "The Winds of Winter" but her request is rejected due to overdue book')

        expected = (library_id, book_id, user_id, date(2022, 1, 13), None, date(2022, 1, 31), 1.0)
        actual = return_book(library_id, book_id, user_id, '2022-01-31')

        self.assertEqual(expected, actual, 'Ada should have checked out on Jan. 13th')
        print('\nAda checks out "The Winds of Winter" on Jan. 13th and returns it in 18 days')


        # Jackie checks out
        user_id = get_user_id('Jackie Gleason')
        book_id = get_book_id('The Winds of Winter')
        checkout_book(2, book_id, user_id, '2022-03-01')

        expected = (2, book_id, user_id, date(2022, 3, 1), None, date(2022, 3, 31), 21.5)
        actual = return_book(2, book_id, user_id, '2022-03-31')

        self.assertEqual(expected, actual, 'Jackie should have checked out on March 1st')
        print('\nJackie checks out "The Winds of Winter" on March 1st and returns it in 30 days')

        # Fairport report
        report = get_all_histories(library_id)
        self.assertEqual(3, report.__len__(), 'Fairport report is incorrect')
        print('\nThe Fairport Librarian runs a report:\n', report)

        #db4 1st output
        print('\nPrinting book checkout table...')
        checkout_table()

        #db4 2nd output
        print('\nGenerating a report...')
        generate_report()

    def test_donate_to_fairport(self):
        library_id = 2
        title = 'The Winds of Winter'
        book_type = 'Fiction'
        author = 'George R.R. Martin'
        copies = 3
        book_id = add_new_book(title, book_type, author, copies)
        add_to_library(library_id, book_id, copies)

        expected = exec_get_one("""
            SELECT book_copies FROM library_stock
            WHERE library_id = %(library_id)s
            AND book_id = %(book_id)s""",
            {'library_id': library_id, 'book_id': book_id})[0]

        self.assertEqual(4, expected, 'Fairport should be 4 copies in total')
        print('\nA good samaritan donates 3 additional copies of the "The Winds of Winter" to Fairport')

    def test_donate_to_pittsford_henrietta(self):
        title = 'The Wines of Winter'
        book_type = 'Fiction'
        author = 'WineExpress'
        copies = 2

        book_id = add_new_book(title, book_type, author, copies)

        add_to_library(3, book_id, 1)
        add_to_library(4, book_id, 1)

        actual = exec_get_all("""
            SELECT * FROM library_stock
            WHERE book_id = %(book_id)s""",
            {'book_id': book_id})

        self.assertEqual(2, actual.__len__(), 'Pittsford and Henrietta should each have 1 copy')
        print('\nAnother good samaritan donates 2 copies of "The Wines of Winter" to Pittsford and Henrietta')

    def test_county_report(self):
        print('\nThe county librarian runs a report listing all books in all libraries:')
        report = report_on_all_libraries()
        self.assertEqual(28, report.__len__(), 'incorrect total books')