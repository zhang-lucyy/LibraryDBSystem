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
    def test_get_art_user_books(self):
        rebuild_tables()
        expected = None
        actual = get_art_user_books()
        print(get_art_user_books())
        self.assertEqual(expected, actual, 'expected empty list from art')

    # Test Case - Listing Jackie Gleason's checked out books in order
    def test_get_gleason_user_books(self):
        actual = get_gleason_user_books()
        expected = [('The Lightning Thief',), ('To Kill a Mockingbird',)]
        self.assertEqual(expected, actual, 'expected books The Lightning Thief and To Kill a Mockingbird are checked out by Gleason')
    