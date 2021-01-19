import binascii
import hashlib
import os


def get_salt():
    '''Generate a random salt for use in the password hash.

    Returns:
        string: The return value. Hex value of the generated salt.
    '''
    salt = os.urandom(16)
    return str(binascii.hexlify(salt).decode('utf-8'))


def hash_password(password, salt):
    '''Create a password hash from the given password and salt.

    Args:
        password: Plain text password.
        salt: Salt in hex form.

    Returns:
        string: The return value. Resulting password hash.
    '''
    key = hashlib.pbkdf2_hmac(
        'sha256', password.encode(), salt.encode(), 100000)
    return str(binascii.hexlify(key).decode('utf-8'))


def check_password(password, hashed, salt):
    '''Check if the provided password matches the original password hash.

    Args:
        password: Plain text password.
        hashed: Hash of the original password.
        salt: Salt in hex form.

    Returns:
        boolean: The return value. Result of the password comparison.
    '''
    return hash_password(password, salt) == hashed
