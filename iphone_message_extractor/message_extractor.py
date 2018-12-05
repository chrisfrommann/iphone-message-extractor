import os
import plistlib as pll
import csv

from .phone_db import PhoneDB, ManifestDB, AddressDB, MessageDB
from . import util

MANIFEST_PLIST_FILENAME = 'Manifest.plist'

def extract_messages(backup_dir, output_path, assumed_country_code):
    """ Primary message extract function that gathers backup info from the Manifest Plist and path data
    (that is, the physical location of the AddressBook.sqlite.db and sms.db files) from the Manifest
    DB, converts the AddressBook to a dict with phone nums as keys, and then maps these onto
    SMS/iMessages before exporting the messages to CSV
    @param backup_dir: the path to the backup/all the goodies (where Manifest.db is)
    @param output_path: the path to write the CSV (or PSV, etc.) output 
    @param assumed_country_code: two-letter country code to assume when numbers lack one
    @return:
    """

    # Ensure that the required manifest files actually exist; otherwise throw an exception
    manifest_plist_path = os.path.join(backup_dir, MANIFEST_PLIST_FILENAME)
    manifest_db_path = os.path.join(backup_dir, PhoneDB.MANIFEST_DB_FILENAME)
    if not os.path.isfile(manifest_plist_path) or not os.path.isfile(manifest_db_path):
        raise FileNotFoundError("Backup is corrupt or in progress (manifest files missing).\
                                 Please verify contents are intact.")
    
    # Determine if this is encrypted before we attempt to read the SQLite DB (this is a value
    # in the Manifest Plist file). Encrypted backups are not [yet] supported
    with open(manifest_plist_path, 'rb') as fp:
        pl = pll.load(fp)
    if pl['IsEncrypted']:
        raise ValueError('This backup is encrypted, but encrypted backups are not (yet) supported')
    
    # Get the real physical paths of the SMS and AddressBook SQLite3 DBS from the ManifestDB
    manifest_db = ManifestDB(manifest_db_path)
    manifest_db.connect()
    sms_db_path = os.path.join(backup_dir, \
                               manifest_db.get_physical_path_for_file(PhoneDB.SMS_DB_FILENAME))
    address_book_db_path = os.path.join(backup_dir, \
                                        manifest_db.get_physical_path_for_file( \
                                            PhoneDB.ADDRESS_BOOK_FILENAME))
    manifest_db.close()

    # Get a dictionary/map of { number/email: [first name, last name] }
    #
    # e.g. {'frodo@shire.net': ['Frodo', 'Baggins'], '+1 212-555-1212': ['Samwise', 'Gamgee'], 
    # '+1 646-555-1212': ['Meriadoc', 'Brandybuck'], '+1 646-400-1212': ['Frodo', 'Baggins']
    address_db = AddressDB(address_book_db_path)
    address_db.connect()
    contacts_dict = address_db.generate_dict_from_address_book()
    address_db.close()
    
    # Retrieve all messages and map on the correct contact name from the contacts_dict above
    message_db = MessageDB(sms_db_path)
    message_db.connect()
    messages = message_db.match_messages_to_contact_dict(contacts_dict)
    message_db.close()
    
    # Dump the messages to the desired output path with a header row
    header_row = ['Last Name', 'First Name', 'Phone #', 'Date & Time', 'Is from me?', \
                  'Message', 'Service']
    write_messages_to_csv(output_path, messages, header_row)


def write_messages_to_csv(output_path, rows, header_row=None, delimiter=','):
    """ Writes a CSV file (or other delimited file) at output_path with given rows and header
    @param output_path: a fully qualified path ending in .csv
    @param rows: a list of 1 or more rows to write to the CSV
    @param header_row: a list of row headers (default=None)
    @param delimiter: the delimiter for file (default=,)
    @return:
    """
    with open(output_path, 'w', encoding='utf-8-sig', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', \
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if header_row is not None:
            csv_writer.writerow(header_row)
                
        csv_writer.writerows(rows)
        
