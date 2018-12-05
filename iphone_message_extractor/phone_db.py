import itertools
import sqlite3
from sqlite3 import Error
from . import util

class PhoneDB():
    """ Very basic base class for working with the iPhone SQLite DB """

    MANIFEST_DB_FILENAME = 'Manifest.db'
    SMS_DB_FILENAME = 'sms.db'
    ADDRESS_BOOK_FILENAME = 'AddressBook.sqlitedb'
    
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
    
    def connect(self):
        """ Opens DB connection to SQLite DB """
        try:
            self.conn = sqlite3.connect(self.db_file)
            return self.conn
        except Error as e:
            print(e)
 
        return None
        
    def close(self):
        """ Closes DB connection to SQLite DB"""
        self.conn.close()

class ManifestDB(PhoneDB):
    """ Class that extends PhoneDB with methods that relate to Manifest.db """
    
    def get_physical_path_for_file(self, file_path):
        """ Gets the physical path in the backup from a filename
        (filenames are basically translated from Library/SMS/sms.db on the device itself
         to something of the form /3d/3d0d7bcef8... in the backup directory) 
        @param file_path: the path you're looking for (e.g. sms.db)
        @return: the fully-qualified path to the file in the backup
        """
        with self.conn:
            cur = self.conn.cursor()
            
            file_id = self.__get_file_id_from_manifest(cur, file_path)
            if file_id is None:
                raise FileNotFoundError("Backup is corrupt or in progress. Failed to find required \
                                        entry in the manifest database. Please verify contents are \
                                        intact.")
            return util.hash_to_path(file_id)        

    def __get_file_id_from_manifest(self, cur, file_path):
        # TODO: fix the assumption that there will only one path ending in sms.db or AddressBook.sqlitedb,
        # which is currently correct, but could easily be broken
        sql = "SELECT fileID, domain, relativePath FROM Files WHERE relativePath LIKE ?"
        cur.execute(sql, ('%' + file_path,))
        result = cur.fetchone()
        return result[0] if result else None


class AddressDB(PhoneDB):
    """ Class that extends PhoneDB with methods that relate to AddressBook.sqlite.db """
    
    def generate_dict_from_address_book(self):
        """ Creates a dictionary from address book entries with *canonicalized* phone numbers
        (or e-mail addresses) as the keys and a tuple with first and last names
        """
        with self.conn:
            cur = self.conn.cursor()
        
            sql = '''
                    SELECT ABPerson.First, ABPerson.Last, ABMultiValue.value
                    FROM ABMultiValue
                    LEFT JOIN ABPerson
                        ON ABMultiValue.record_id = ABPerson.ROWID
                    WHERE value IS NOT NULL
                  '''
            res = cur.execute(sql)
            # col_name_list = [tuple[0] for tuple in res.description]
            
            rows = cur.fetchall()
        
            key_function = lambda r: util.normalize_contact_value(r[2])
            
            return dict((key_function(row), (row[0], row[1])) for row in rows)

class MessageDB(PhoneDB):
    """ Class that extends PhoneDB with methods that relate to sms.db """
    
    def match_messages_to_contact_dict(self, contact_dict):
        """ Maps the phone number/e-mail of each message (the "handle.id") to an address book
        entry from the contact_dict dictionary/hash
        @param contact_dict: the dictionary of phone numbers to names
        @return: a list of messages with names appended
        """
        with self.conn:
            cur = self.conn.cursor()
        
            # See here https://stackoverflow.com/questions/10746562/parsing-date-field-of-iphone-sms-file-from-backup
            # for an explanation of the iPhone date handling
            sql = '''
                    SELECT handle.id as handle,
                           -- as recorded, message.date has 9 extra zeros and the offset
                           -- is from 2001-01-01 instead of 1970-01-01
                           substr(message.date, 1, 9) + strftime('%s', '2001-01-01 00:00:00')
                               as unix_timestamp,
                           (CASE WHEN message.is_from_me THEN 'Yes' ELSE 'No' END) as is_from_me,
                           message.text, handle.service as service
                    FROM message
                    INNER JOIN handle
                        ON handle.ROWID = message.handle_id
                    ORDER BY handle.id, message.date
                  '''
            res = cur.execute(sql)
            # col_name_list = [tuple[0] for tuple in res.description]
        
            rows = cur.fetchall()
            return list(map(MessageDB.__map_message_to_contact, rows, \
                                itertools.repeat(contact_dict, len(rows)) ))
    
    def __map_message_to_contact(row, contacts_dict):
        contact_key = util.normalize_contact_value(row[0])
        name_tuple = contacts_dict[contact_key] if contact_key in contacts_dict else None 
    
        if name_tuple is None:
            name_tuple = ['', '']
        return [name_tuple[1], name_tuple[0], contact_key,
                util.convert_timestamp_to_date(row[1])] + list(row[2:])