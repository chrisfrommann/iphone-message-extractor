#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
iPhone Message Extractor
========================

Simple CLI written in python to extract messages (SMS/iMessage) to CSV from iPhone backups

"""

import argparse
import os, re

from iphone_message_extractor.message_extractor import extract_messages

def main():

    # Set up the arg parser with appropriate help text
    parser = argparse.ArgumentParser(description="Extracts messages (SMS/iMessage) to CSV from \
                                                 iPhone backups")
    device_hash_help_text = """
                            The 40 character device hash identifying the backup you'd like to use.
                            This can be found by going to iTunes > Preferences > Devices and right
                            clicking the backup you wish to extract and selecting 'Show in Finder'.
                            It will be 40 characters and look like 
                            '9504c9835a9fcd2da71a23b42cd4e7c971a23842'
                            """
    parser.add_argument("device_hash", help=device_hash_help_text) # nargs='+', 
    parser.add_argument("output_path", help="The full output path to where you would like to store\
                                             the CSV")
    parser.add_argument("-v", "--verbose", help="Make output more verbose", action="store_true")
    country_code_help_text = """
                             The country code to apply for phone numbers without them (defaults to
                             USA). For example, 555-555-5555 will become +1-555-555-5555. Numbers
                             with country codes (eg. +49-17-555-55555) will be unaffected.
                             """
    parser.add_argument("-c", "--country", help=country_code_help_text)
    parser.add_argument("-d", "--backup-dir", help="Path to backup directory (if non-standard)")
    args = parser.parse_args()

    # Either take the path provided or use the defaults on macOS and Windows (path must
    # be provided for Linux)
    backup_dir = args.backup_dir or util.get_backup_dir()
    if backup_dir is None:
        print("Can't guess the location of your backups; please specify a path with -p")
        return

    # If a country code was provided, verify it makes sense
    country_code = args.country or 'US'
    if not re.match(r"^[A-Z]{2}$", country_code):
        print("Invalid country code (must be 2 characters; e.g. GB for Great Britain)")
        return

    # Check that the db path is in fact valid
    device_hash = args.device_hash
    backup_dir = os.path.join(backup_dir, args.device_hash)
    if not os.path.exists(backup_dir):
        print("Backup path isn't valid. Check path or device hash.")
        return

    # Let's actually extract the messages to the specified backup path
    print("Extracting messages...")
    extract_messages(backup_dir=backup_dir,\
                     output_path=args.output_path,\
                     assumed_country_code=country_code)
    print("Done. File at: {}".format(args.output_path))
 
if __name__ == '__main__':
    main()


