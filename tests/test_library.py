import datetime
import unittest
from src.swen344_db_utils import *
from src.library import *

class TestLibrary(unittest.TestCase):
    
    def set_up():
        rebuild_tables()

    def test_verify_users_rows(self):
        expected = 4
        actual = get_all_users().__len__()
        self.assertEqual(expected, actual, "incorrect count of rows for users table")
        print("\nNumber of rows in users table:", actual)

    def test_verify_inventory_rows(self):
        expected = 9
        actual = get_nonfiction_books().__len__() + get_fiction_books().__len__()
        self.assertEqual(expected, actual, "incorrect count of rows for inventory table")
        print("\nNumber of rows in inventory table:", actual)

    def test_verify_checkout_rows(self):
        expected = 5
        actual = get_checked_out_books().__len__()
        self.assertEqual(expected, actual, "incorrect count of rows for checkout table")
        print("\nNumber of rows in checkout table:", actual)

    def test_get_user_contact_info(self):
        expected = 'ALovelace@gmail.com'
        actual = get_user_contact_info(1)[0];
        self.assertEqual(expected, actual, "Ada Lovelace's contact info is incorrect")
        print("\nAda Lovelace's contact info:", actual)

    def test_get_user_books_art(self):
        rebuild_tables()
        expected = []
        actual = get_user_books(4)
        self.assertEqual(expected, actual, "expected empty list from art")
        print("\nArt's checked out books:", actual)

    def test_get_user_books_gleason(self):
        expected = 2
        actual = get_user_books(3)
        self.assertEqual(expected, actual.__len__(), "expected books The Lightning Thief and To Kill a Mockingbird are checked out by Gleason")
        print("\nJackie Gleason's checked out books in alphabetical order:", actual)

    def test_get_nonfiction_books(self):
        expected = 4
        actual = get_nonfiction_books()
        self.assertEqual(expected, actual.__len__(), "not all expected non-fiction books are listed")
        print("\nAll non-fiction books:", actual)

    def test_get_fiction_books(self):
        expected = 5
        actual = get_fiction_books()
        self.assertEqual(expected, actual.__len__(), "not all expected fiction books are listed")
        print("\nAll fiction books:", actual)

    def test_search_by_author(self):
        expected = ('To Kill a Mockingbird', 'Fiction', 'Harper Lee', 1960, 1)
        actual = search_by_author('Harper Lee')[0]
        self.assertEqual(expected, actual, "not all books by Harper Lee are listed")
        print("\nBooks in inventory by Harper Lee:", actual)

    def test_create_account(self):
        create_account('Christopher Marlowe', 'CMarlowe@gmail.com')
        expected1 = [(5, 'Christopher Marlowe', 'CMarlowe@gmail.com')]
        actual1 = exec_get_all("""
            SELECT * From users WHERE name = \'Christopher Marlowe\'
        """)

        create_account('Francis Bacon', 'FBacon@gmail.com')
        expected2 = [(6, 'Francis Bacon', 'FBacon@gmail.com')]
        actual2 = exec_get_all("""
            SELECT * From users WHERE name = \'Francis Bacon\'
        """)

        self.assertEqual(expected1, actual1, "did not create an account for Christopher Marlowe")
        self.assertEqual(expected2, actual2, "did not create an account for Francis Bacon")
        print("\nChristopher Marlowe and Francis Bacon each sign up for a new account")

    def test_reserve_book_fail(self):
        user_id = get_user_id('Jackie Gleason')
        book_id = get_book_id('Figuring')

        with self.assertRaises(Exception) as cannot_reserve:
            reserve_book(book_id, user_id)
            self.assertTrue('Copies are still available' in cannot_reserve.exception)
        print("\nJackie Gleason reserves a book incorrectly")

    def test_reserve_book_success(self):
        user_id = get_user_id('Jackie Gleason')
        book_id = get_book_id('The Lord of the Rings')
        reserve_book(book_id, user_id)
        expected = [(6, 3)]
        actual = exec_get_all("""
            SELECT * From reserve WHERE user_id = %(user_id)s""",
            {'user_id': user_id})

        self.assertEqual(expected, actual, "did not successfully reserve a book")
        print("\nJackie Gleason successfully reserves a book")

    def test_return_book(self):
        user_id = get_user_id('Art Garfunkel')
        book_id = get_book_id("Frankenstein")
        checkout_book(book_id, user_id, '2020-09-10')
        return_book(book_id, user_id, '2020-09-13')
        expected = [(9, 4, datetime.date(2020, 9, 10), datetime.date(2020, 9, 13))]
        actual = exec_get_all("""
            SELECT * From checkout WHERE user_id = %(user_id)s""",
            {'user_id': user_id})

        self.assertEqual(expected, actual, "Art did not return the book")
        print('\nArt Garfunkel returns a copy of “Frankenstein” three days after he borrowed it')

    def test_delete_account(self):
        return_book(3, 2, '2020-09-10')
        delete_account('Mary Shelley')
        expected = []
        actual = exec_get_all("""
            SELECT * From users WHERE name = 'Mary Shelley'
        """)

        self.assertEqual(expected, search_by_title('The Last Man'))
        self.assertEqual(expected, actual, "Mary Shelley's account should be deleted")
        print('\nMary Shelley deletes her account after finding no copies of "The Last Man" in the library')

    def test_get_checked_out_books(self):
        expected = 3
        actual = get_checked_out_books()
        self.assertEqual(expected, actual.__len__(), "not all checked out books are listed")
        print("\nThe librarian gets a list of all books checked out:", actual)