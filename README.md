# iPhone Message Extractor

Simple CLI written in Python to extract messages (SMS/iMessage) to CSV from iPhone backups.
Apologies if my Python is rusty; it's been a while.

As a note, this is (deliberately) not yet available via setuptools.


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

    source ./venv/bin/activate

    python -m unittest discover

Release Notes:
===
New in version 0.1.1: 
* Emojis actually work (very important, I know)! 🎉
* Added fixtures and integration tests for `phone_db.py`

New in version 0.1.0:
* Basic CLI works!

TODO
===
Planned features, in rough priority:

* Support for group conversations
* Get working for encrypted backups
* Add support for images
* Make verbosity actually do something
* Pull voicemail
* E2E test for `message_extractor.py`
* Add some sort of progress spinner to indicate the script is doing work
* Fix emoji output
