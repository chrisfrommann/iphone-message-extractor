import csv, os

from iphone_message_extractor.phone_db import PhoneDB, ManifestDB, AddressDB, MessageDB

#
#   Helper methods to create in-memory SQLite3 fixtures:
#

def create_db(klass, func):
    '''' Wrapper method that takes and creates the right type of PhoneDB and runs SQL on it
    @param klass: the class that should be instantiated with the methods needed
    @param func: a function to execute the SQL
    @returns: the db connection
    '''
    db = klass(':memory:')
    conn = db.connect()
    with conn:
        cursor = conn.cursor()
        func(cursor)
    conn.commit()
    
    return db

def create_manifest_db():
    # Create in-memory ManifestDB
    def manifest_sql(cur):
        # Create Files table
        cur.execute('CREATE TABLE Files(fileID TEXT PRIMARY KEY, domain TEXT, relativePath TEXT);')
        # Insert files we care about
        sql = ''' INSERT INTO Files(fileID, domain, relativePath)
                      VALUES('469af719d01883a826c1bb5e834aafde3e8d5c33',
                              'HomeDomain', 'Library/SMS/sms.db'),
                             ('c18c568fb88c22ab4a6b464aba8474edd2586ad4',
                              'HomeDomain', 'Library/AddressBook/AddressBook.sqlitedb')
              '''
        cur.execute(sql)
    
    return create_db(ManifestDB, manifest_sql)
    
    
def create_address_book_db():
    # Create in-memory AddressDB
    def address_sql(cur):
        # Create ABPerson table
        create_person_table_sql = '''
          CREATE TABLE ABPerson (
             ROWID	INTEGER, First	TEXT, Last	TEXT, Middle	TEXT, FirstPhonetic	TEXT,
             MiddlePhonetic	TEXT, LastPhonetic	TEXT, Organization	TEXT,
             Department	TEXT, Note	TEXT, Kind	INTEGER, Birthday	TEXT,
             JobTitle	TEXT, Nickname	TEXT, Prefix	TEXT, Suffix	TEXT,
             FirstSort	TEXT, LastSort	TEXT, CreationDate	INTEGER,
             ModificationDate	INTEGER, CompositeNameFallback	TEXT,
             ExternalIdentifier	TEXT, ExternalModificationTag	TEXT,
             ExternalUUID	TEXT, StoreID	INTEGER, DisplayName	TEXT,
             ExternalRepresentation	BLOB, FirstSortSection	TEXT, LastSortSection	TEXT,
             FirstSortLanguageIndex	INTEGER, LastSortLanguageIndex	INTEGER,
             PersonLink	INTEGER, ImageURI	TEXT, IsPreferredName	INTEGER, guid	TEXT,
             PhonemeData	TEXT, AlternateBirthday	TEXT, MapsData	TEXT,
             FirstPronunciation	TEXT, MiddlePronunciation	TEXT, LastPronunciation	TEXT,
             OrganizationPhonetic	TEXT, OrganizationPronunciation	TEXT,
             PreviousFamilyName	TEXT, PreferredLikenessSource	TEXT,
             PreferredPersonaIdentifier	TEXT);
        '''
        cur.execute(create_person_table_sql)
        
        populate_people_sql = ''' INSERT INTO ABPerson(ROWID, First, Last)
                                  VALUES(1, 'Frodo', 'Baggins'), (2, 'Samwise','Gamgee'),
                                  (3, 'Meriadoc', 'Brandybuck'), (4, 'Bilbo', 'Baggins'),
                                  (5, 'Gandalf', 'the Grey') '''
        cur.execute(populate_people_sql)
        
        create_multi_val_table_sql = ''' CREATE TABLE ABMultiValue(
                                         UID	INTEGER, record_id	INTEGER,
                                         property	INTEGER, identifier	INTEGER,
                                         label	INTEGER, value	TEXT, guid	TEXT) '''
        cur.execute(create_multi_val_table_sql)
        
        populate_people_sql = ''' INSERT INTO ABMultiValue(record_id, value)
                                      VALUES(1, 'frodo@shire.net'), (1, '(646) 400-1212'),
                                            (2, '+1 212-555-1212'), (3, '646.555.1212'),
                                            (4, '415 555 1212'),  (5, 'mithrandir@gondor.net')'''
        cur.execute(populate_people_sql)
    
    return create_db(AddressDB, address_sql)
    
    
def create_message_db():
    # Create in-memory MessageDB
    def message_sql(cur):
        
        create_message_table_sql = '''
          CREATE TABLE message (
            guid	TEXT, text	TEXT, replace	INTEGER, service_center	TEXT, handle_id	INTEGER,
            subject	TEXT, country	TEXT, attributedBody	BLOB, version	INTEGER,
            type	INTEGER, service	TEXT, account	TEXT, account_guid	TEXT, error	INTEGER,
            date	INTEGER, date_read	INTEGER, date_delivered	INTEGER, is_delivered	INTEGER,
            is_finished	INTEGER, is_emote	INTEGER, is_from_me	INTEGER, is_empty	INTEGER,
            is_delayed	INTEGER, is_auto_reply	INTEGER, is_prepared	INTEGER,
            is_read	INTEGER, is_system_message	INTEGER, is_sent	INTEGER,
            has_dd_results	INTEGER, is_service_message	INTEGER, is_forward	INTEGER,
            was_downgraded	INTEGER, is_archive	INTEGER, cache_has_attachments	INTEGER,
            cache_roomnames	TEXT, was_data_detected	INTEGER, was_deduplicated	INTEGER,
            is_audio_message	INTEGER, is_played	INTEGER, date_played	INTEGER,
            item_type	INTEGER, other_handle	INTEGER, group_title	TEXT,
            group_action_type	INTEGER, share_status	INTEGER, share_direction	INTEGER,
            is_expirable	INTEGER, expire_state	INTEGER, message_action_type	INTEGER,
            message_source	INTEGER, associated_message_guid	STRING,
            balloon_bundle_id	STRING, payload_data	BLOB, associated_message_type	INTEGER,
            expressive_send_style_id	STRING, associated_message_range_location	INTEGER,
            associated_message_range_length	INTEGER, time_expressive_send_played	INTEGER,
            message_summary_info	BLOB, ck_sync_state	INTEGER, ck_record_id	TEXT,
            ck_record_change_tag	TEXT, destination_caller_id	TEXT, sr_ck_sync_state	INTEGER,
            sr_ck_record_id	TEXT, sr_ck_record_change_tag	TEXT);
        '''
        cur.execute(create_message_table_sql)
        
        create_handle_table_sql = '''
          CREATE TABLE handle (
            ROWID	INTEGER, id	TEXT, country	TEXT, service	TEXT,
            uncanonicalized_id	TEXT);
        '''
        
        cur.execute(create_handle_table_sql)
        
        populate_handles_sql = ''' INSERT INTO handle(ROWID, id, service)
                                      VALUES(1, 'mailto:frodo@shire.net', 'iMessage'),
                                            (2, '646-400-1212', 'iMessage'),
                                            (3, '+1 (212) 555-1212', 'iMessage'),
                                            (4, '646 555 1212', 'iMessage'),
                                            (5, 'tel:415-555-1212', 'iMessage'),
                                            (6, 'mailto:mithrandir@gondor.net', 'iMessage') '''
                                            
        cur.execute(populate_handles_sql)
        
        # message.handle_id (ROWID), date, is_from_me, text
        messages = [[3, '345988810', True, "Mordor! I hope the others find a safer road."],
                    [3, '345988845', False, "Strider'll look after them."],
                    [3, '345988880', True, "I don't suppose we'll ever see them again."],
                    [3, '345988900', False, "We may yet, Mr. Frodo. We may."],
                    [3, '345988920', True, "Sam? I'm glad you're with me."],
                    [6, '345992930', True, "I wish the ring had never come to me, I wish none " + \
                        "of this had happened."],
                    [6, '345992930', True, "So do all who live to see such times, but that is " + \
                        "not for us to decide. All we have to decide is what to do with the time " + \
                        "that's been given us."]]
        
        for message in messages:
            message[1] = "{}{}".format(message[1], '0' * 9)
            cur.execute(''' INSERT INTO message(handle_id, date, is_from_me, text)
                            VALUES(?, ?, ?, ?)
                        ''', message)
        
    
    return create_db(MessageDB, message_sql)
    
def read_expected_output():
    ''' Reads the expected output and returns as an array of arrays '''
    rows = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'expected_messages.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        saw_header = False
        line_count = 0
        for row in csv_reader:
            if saw_header == False:
                saw_header = True
            else:
                rows.append(row)
    return rows