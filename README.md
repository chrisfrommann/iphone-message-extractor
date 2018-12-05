# iPhone Message Extractor

Simple CLI written in Python to extract messages (SMS/iMessage) to CSV from iPhone backups.
Apologies if my Python is rusty; it's been a while.


Setup
====
After cloning run `pip3 install virtualenv` and then set up your virtual environment

    virtualenv -p python3 venv

(.If you have trouble building the virtalenv, try running `pip3 install --upgrade pip`
and `pip3 install --upgrade setuptools` to install the latest version of `pip3` and
`setuptools` respectively.)

Active the virtual environment by running:

    source ./venv/bin/activate

Then install the necessary dependencies.

    pip3 install -r requirements.txt
    
Running
====
Ensure that you are using your virtual environment (see above)

    source ./venv/bin/activate

Then run

    ./iphone_message_extractor.py [-v] [-c COUNTRY] [-p BACKUP_PATH] device_hash output_path
    
Run `./iphone_message_extractor.py -h` for a full explanation of options

Running tests
====
    python -m unittest discover

Release Notes:
===
New in version 0.1.1: 
* Emojis actually work (very important, I know)!

New in version 0.1.0:
* Basic CLI works!

TODO
===
* Integration tests for `phone_db.py`
    * will need to mock/make fixtures
* E2E test for `message_extractor.py`
* Make verbosity actually do something
* Add some sort of progress spinner to indicate the script is doing work
* Get working for encrypted backups
* Fix emoji output
* Add support for images
* Add suport for group chats


Some data notes (TODO: put actual schemas)
===

##### ABMultiValue:

        ['UID', 'record_id', 'property', 'identifier', 'label', 'value', 'guid']
        
##### ABPerson:

        ['ROWID', 'First', 'Last', 'Middle', 'FirstPhonetic', 'MiddlePhonetic', 'LastPhonetic', 'Organization', 
        'Department', 'Note', 'Kind', 'Birthday', 'JobTitle', 'Nickname', 'Prefix', 'Suffix', 'FirstSort', 'LastSort',
        'CreationDate', 'ModificationDate', 'CompositeNameFallback', 'ExternalIdentifier', 'ExternalModificationTag',
        'ExternalUUID', 'StoreID', 'DisplayName', 'ExternalRepresentation', 'FirstSortSection', 'LastSortSection',
        'FirstSortLanguageIndex', 'LastSortLanguageIndex', 'PersonLink', 'ImageURI', 'IsPreferredName', 'guid',
        'PhonemeData', 'AlternateBirthday', 'MapsData', 'FirstPronunciation', 'MiddlePronunciation',
        'LastPronunciation', 'OrganizationPhonetic', 'OrganizationPronunciation', 'PreviousFamilyName',
        'PreferredLikenessSource', 'PreferredPersonaIdentifier']
        
##### messages

        'ROWID', 'guid', 'text', 'replace', 'service_center', 'handle_id', 'subject', 'country', 'attributedBody',
        'version', 'type', 'service', 'account', 'account_guid', 'error', 'date', 'date_read', 'date_delivered',
        'is_delivered', 'is_finished', 'is_emote', 'is_from_me', 'is_empty', 'is_delayed', 'is_auto_reply',
        'is_prepared', 'is_read', 'is_system_message', 'is_sent', 'has_dd_results', 'is_service_message', 'is_forward',
        'was_downgraded', 'is_archive', 'cache_has_attachments', 'cache_roomnames', 'was_data_detected',
        'was_deduplicated', 'is_audio_message', 'is_played', 'date_played', 'item_type', 'other_handle', 'group_title',
        'group_action_type', 'share_status', 'share_direction', 'is_expirable', 'expire_state', 'message_action_type',
        'message_source', 'associated_message_guid', 'balloon_bundle_id', 'payload_data', 'associated_message_type',
        'expressive_send_style_id', 'associated_message_range_location', 'associated_message_range_length',
        'time_expressive_send_played', 'message_summary_info', 'ck_sync_state', 'ck_record_id', 'ck_record_change_tag',
        'destination_caller_id', 'sr_ck_sync_state', 'sr_ck_record_id', 'sr_ck_record_change_tag'