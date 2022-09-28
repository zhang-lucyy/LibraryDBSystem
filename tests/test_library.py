import unittest
from src.swen344_db_utils import *
from src.library import *

class TestLibrary(unittest.TestCase):
    
    def set_up(self):
        rebuild_tables()

    def test_verify_users_rows(self):
        expected = 4
        actual = get_all_users().__len__()
        self.assertEqual(expected, actual, "incorrect count of rows for users table")
        print("\nNumber of rows in users table:", actual)

    def test_verify_inventory_rows(self):
        expected = 8
        actual = get_nonfiction_books().__len__() + get_fiction_books().__len__()
        self.assertEqual(expected, actual, "incorrect count of rows for inventory table")
        print("\nNumber of rows in inventory table:", actual)

    def test_verify_checkout_rows(self):
        expected = 4
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
    
    def test_get_checked_out_books(self):
        expected = 4
        actual = get_checked_out_books()
        self.assertEqual(expected, actual.__len__(), "not all checked out books are listed")
        print("\nAll checked out books ordered by user name:", actual)

    def test_get_nonfiction_books(self):
        expected = 4
        actual = get_nonfiction_books()
        self.assertEqual(expected, actual.__len__(), "not all expected non-fiction books are listed")
        print("\nAll non-fiction books:", actual)

    def test_get_fiction_books(self):
        expected = 4
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