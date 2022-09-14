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
        actual_users = get_all_users()
        expected_users = [(1, 'Ada Lovelace'), (2, 'Mary Shelley'), 
        (3, 'Jackie Gleason'), (4, 'Art Garfunkel')]
        self.assertEqual(expected_users, actual_users, 'expected users not in table')

    # Test Case - Art's checked out books returns an empty list
    def test_get_art_user_books(self):
        rebuild_tables()
        expected_output = None
        actual_output = get_art_user_books()
        print(get_art_user_books())
        self.assertEqual(expected_output, actual_output, 'expected empty list from art')

    # Test Case - Listing Jackie Gleason's checked out books in order
    # add more books to Gleaosn's list
    def test_get_gleason_user_books(self):
        actual_output = get_gleason_user_books()[0]
        expected_output = "The Lightning Thief"
        self.assertEqual(expected_output, actual_output, 'expected book The Lightning Thief to be checked out by Gleason')
    