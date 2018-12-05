import os, platform, re
from datetime import datetime, date
import time
import phonenumbers
from os.path import expanduser

PROBABLE_PHONE_RE = re.compile(r"(tel:)?[\+\(\)\-\. 0-9]+")

def hash_to_path(hash):
    """ iTunes stores backup files in a dir that matches the first 2 chars of the hash; this
    generates this path (e.g. 3d0d7bcef8... -> /3d/3d0d7bcef8...) """
    return os.path.join(hash[:2], hash)
    
def normalize_contact_value(val):
    """ Detect whether something is likely an e-mail or phone number and then normalize it """
    probable_phone_re = re.compile(r"(tel:)?[\+\(\)\-\. 0-9]+")
    
    if '@' in val:
        return normalize_email(val)
    elif re.match(PROBABLE_PHONE_RE, val):
        return normalize_phone(val)
    else:
    # this is either a URL, or name or something we can't use (e.g. partner shows up here)
        print("Warning: couldn't make sense of '{}' as a phone number or e-mail".format(val))
        return None

def normalize_email(email):
    """ Strip mailto: from e-mails (don't know why this is sometimes present...) """
    return email.replace('mailto:', '')
    
def normalize_phone(orig_phone_num, assumed_country_code='US'):
    """ Remove all non-numeric values (or +) and standardize per the Google phone numbers library
    @param orig_phone: Guess :p
    @param assumed_country_code: The country code to apply when # is lacking one (your home country)
    @return: a number in standard international/E164 format (e.g. +1 212 555 1212)
    """
    phone = re.sub(r"(^ +)|( +$)|(^tel:)", "", re.sub(r"[^\+0-9]+", " ", orig_phone_num))
    # Use the python port of Google's libphonenumber library to parse
    # and standardize/canonicalize international phone numbers
    try:
        return parse_phone_number(phone)
    except phonenumbers.phonenumberutil.NumberParseException:
        try:
            # Try again making the explicit assumption of a US number
            return parse_phone_number(phone, assumed_country_code)
        except phonenumbers.phonenumberutil.NumberParseException:
            print('Warning: unparseable number encountered: {}'.format(orig_phone_num))
    return None
    
def parse_phone_number(phone, region=None):
    """ Helper method that takes a striped phone # and sends it through the phonenumbers lib """
    parsed_num = phonenumbers.parse(phone, region)
    if phonenumbers.is_possible_number(parsed_num):
        return phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    return None
    
def convert_timestamp_to_date(ts):
    """ Unix timestamp (1970, from Apple time from not 2001) to string representation of date """
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
def get_backup_dir():
    """ Returns the default backup directory for macOS or Windows """
    home_path = expanduser("~")
    if platform.system() == 'Darwin':
        return os.path.join(home_path, "Library/Application Support/MobileSync/Backup")
    elif platform.system() == 'Windows':
        return os.path.join(home_path, "AppData\\Roaming\\Apple Computer\\MobileSync\\Backup\\")
    return None