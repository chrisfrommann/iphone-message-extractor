import os
from unittest import TestCase, main

from iphone_message_extractor import util
from iphone_message_extractor.phone_db import PhoneDB, ManifestDB, AddressDB, MessageDB
from . import fixtures

class TestPhoneDB(TestCase):
    '''
    Integration tests to ensure functionality of various classes in phone_db.
    Fixtures are generated once for the class instead of per test since in reality
    we aren't modifying these DBs in the application code either. See fixtures.py
    for code to generate dummy data.
    '''
    
    @classmethod
    def setUpClass(klass):
        klass.manifest_db = fixtures.create_manifest_db()
        klass.address_db = fixtures.create_address_book_db()
        klass.message_db = fixtures.create_message_db()
 
    @classmethod
    def tearDownClass(klass):
        klass.manifest_db.close()
        klass.address_db.close()
        klass.message_db.close()
    
    def test_manifest_get_sms_db(self):
        ''' Ensure the proper DB path is returned from the Manifest '''
        self.assertEqual(TestPhoneDB.manifest_db.get_physical_path_for_file(PhoneDB.SMS_DB_FILENAME),\
                         '46/469af719d01883a826c1bb5e834aafde3e8d5c33')
                         
    def test_manifest_missing_file(self):
        ''' Make sure we throw an exception when we try to look up a file that isn't there '''
        with self.assertRaises(FileNotFoundError):
            TestPhoneDB.manifest_db.get_physical_path_for_file('com.apple.Preferences.plist')

    def __expected_dict(self):
         return {'frodo@shire.net': ('Frodo', 'Baggins'),
                 '+1 646-400-1212': ('Frodo', 'Baggins'),
                 '+1 212-555-1212': ('Samwise', 'Gamgee'),
                 '+1 646-555-1212': ('Meriadoc', 'Brandybuck'),
                 '+1 415-555-1212': ('Bilbo', 'Baggins'),
                 'mithrandir@gondor.net': ('Gandalf', 'the Grey')}
                     
    def test_address_book_dict(self):
        ''' Ensure the address book dict is being properly generated '''
        self.assertEqual(TestPhoneDB.address_db.generate_dict_from_address_book(),
                         self.__expected_dict())
       
    def test_address_book_unknown_val(self):
        ''' Test that an invalid entry does not change the address dict '''
        # add an unparseable value to the address_db
        conn = TestPhoneDB.address_db.connection()
        with conn:
            cur = conn.cursor()
            sql = "INSERT INTO ABMultiValue(record_id, value) VALUES(5, 'http://mithrandir.net')"
            res = cur.execute(sql)
        conn.commit()
        
        # We should still have the same dictionary since we have added an unparseable value
        self.assertEqual(TestPhoneDB.address_db.generate_dict_from_address_book(),
                        self.__expected_dict())
        
        # clean up after ourselves since the address db is set up/torn down for the whole
        # class, not per test (might change in the future as necessary...)
        with conn:
            res = cur.execute("DELETE FROM ABMultiValue WHERE value = 'http://mithrandir.net'")
        conn.commit()
        
    def test_matching_messages_to_contact_dict(self):
        ''' Ensure that match_messages_to_contact_dict matches to the right contacts '''
        expected_output = fixtures.read_expected_output()
        
        self.assertEqual(expected_output,\
                    TestPhoneDB.message_db.match_messages_to_contact_dict(self.__expected_dict()))
        
        
if __name__ == '__main__':
    unittest.main()