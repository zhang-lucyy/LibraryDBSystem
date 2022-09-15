import unittest
from src.swen344_db_utils import *
from src.library import *

class TestLibrary(unittest.TestCase):
    
    def setUp(self):
        rebuild_tables()

    #def test_rebuild_tables(self):
        #"""Build the tables"""
        #conn = connect()
        #cur = conn.cursor()
        #rebuild_tables()
        #cur.execute('SELECT * FROM users')
        #self.assertEqual([], cur.fetchall(), "no rows in users")
        #conn.close()

    #def test_rebuild_tables_is_idempotent(self):
        #"""Drop and rebuild the tables twice"""
        #rebuild_tables()
        #rebuild_tables()
        #conn = connect()
        #cur = conn.cursor()
        #cur.execute('SELECT * FROM users')
        #self.assertEqual([], cur.fetchall(), "no rows in users")
        #conn.close()
 
    def test_number_of_users(self):
        "Check correct number of users in rows"
        actual = get_all_users()
        expected = [(1, 'Ada Lovelace'), (2, 'Mary Shelley'), 
        (3, 'Jackie Gleason'), (4, 'Art Garfunkel')]
        self.assertEqual(expected, actual, 'expected users not in table')

    # Test Case - Art's checked out books returns an empty list
    def test_get_user_books_art(self):
        rebuild_tables()
        expected = []
        actual = get_user_books(4)
        self.assertEqual(expected, actual, 'expected empty list from art')

    # Test Case - Listing Jackie Gleason's checked out books in order
    def test_get_user_books_gleason(self):
        actual = get_user_books(3)
        expected = [('The Lightning Thief', 'Fiction', 'Rick Riordan', 2005), 
            ('To Kill a Mockingbird', 'Fiction', 'Harper Lee', 1960)]
        self.assertEqual(expected, actual, 'expected books The Lightning Thief and To Kill a Mockingbird are checked out by Gleason')
    
    # Test Case 
    def test_get_checked_out_books(self):
        actual = get_checked_out_books()
        expected = [('In Defence of Witches', 'Non-fiction', 'Mona Chollet'),
            ('The Lightning Thief', 'Fiction', 'Rick Riordan'),
            ('To Kill a Mockingbird', 'Fiction', 'Harper Lee'),
            ('Scary Smart', 'Non-fiction', 'Mo Gawdat')]
        self.assertEqual(expected, actual, 'not all checked out books are listed')

    # Test Case - List all the non-fiction books in inventory, along with the quantity
    def test_get_nonfiction_books(self):
        actual = get_nonfiction_books()
        expected = [('Figuring', 'Non-fiction', 'Maria Popova', 5),
            ('In Defence of Witches', 'Non-fiction', 'Mona Chollet', 3),
            ('Scary Smart', 'Non-fiction', 'Mo Gawdat', 7),
            ('The Princess Spy', 'Non-fiction', 'Larry Loftis', 2)]
        self.assertEqual(expected, actual, 'not all expected non-fiction books are listed')

    # Additional Test Case - List all the fiction books in inventory, along with the quantity
    def test_get_fiction_books(self):
        actual = get_fiction_books()
        expected = [('The Dead Romantics', 'Fiction', 'Ashley Poston', 6),
            ('The Lord of the Rings', 'Fiction', 'J.R.R. Tolkien', 9),
            ('The Lightning Thief', 'Fiction', 'Rick Riordan', 4),
            ('To Kill a Mockingbird', 'Fiction', 'Harper Lee', 1)]
        self.assertEqual(expected, actual, 'not all expected fiction books are listed')