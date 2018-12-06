import os
from unittest import TestCase, main

from iphone_message_extractor import util

class TestUtil(TestCase):
    
    def test_hash_to_path_valid(self):
        # hash_to_path used to do more, but this is now kinda dumb...
        hash_val = '3d0d7e5fb2ce288813306e4d4636395e047a3d28'
        self.assertEqual(util.hash_to_path(hash_val),
                         os.path.join('3d', '3d0d7e5fb2ce288813306e4d4636395e047a3d28'))

    def test_normalize_contact_value_with_url(self):
        contact_val = 'http://www.apple.com'
        self.assertTrue(util.normalize_contact_value(contact_val) is None)
    
    def test_normalize_email(self):
        # this method also used to do more...
        email = 'frodo@baggins.net'
        self.assertEqual(util.normalize_email('mailto:{}'.format(email)), email)
        
    def test_normalize_phone_valid_nums(self):
        good_phones = [('tel:+13475551212', '+1 347-555-1212'),
                       ('+49 55520401212', '+49 5552 0401212'),
                       ('(415) 555-1212', '+1 415-555-1212'),
                       ('415.555.1212', '+1 415-555-1212'),
                       ('4155551212', '+1 415-555-1212'),
                       ('650-555-1212', '+1 650-555-1212'),
                       ('+1 646-555-1212', '+1 646-555-1212'),
                       ('+1 (406) 555-1212', '+1 406-555-1212'),
                       ('+445000521212', '+44 50 0052 1212')]
        for phone_tuple in good_phones:
            self.assertEqual(util.normalize_phone(phone_tuple[0]), phone_tuple[1])
        
    def test_normalize_phone_invalid_nums(self):
        bad_phones = ['1 (650) 555-1212,626626262#', '34 98 72', '415 555 121', '21']
        for num in bad_phones:
            self.assertEqual(util.normalize_phone(num), None)  
    
if __name__ == '__main__':
    unittest.main()