#!/usr/bin/env python3
"""
Script to crack PBKDF2 password hash
"""

from werkzeug.security import check_password_hash
import itertools
import string

# The hash you provided
target_hash = "pbkdf2:sha256:600000$5nMCcRBXZ0XCR3pC$1f57c050daa7028f8971473db2f78818d0ea49ef92be64786b520a757ed6d58f"

# Common passwords to try
common_passwords = [
    'admin123',
    'admin',
    'password',
    '123456',
    'admin1',
    'admin2023',
    'admin2024',
    'hoahuongduong',
    'hoa123',
    'duong123',
    'password123',
    '12345678',
    'qwerty',
    'abc123',
    'admin@123',
    'root',
    'toor',
    'administrator',
    'pass',
    'test',
    'demo',
    'guest',
    'user',
    '1234',
    '12345',
    '123456789',
    'password1',
    'admin321',
    'secret',
    'welcome',
    'login',
    'master',
    'super',
    'system',
    'default',
    'changeme',
    'temp',
    'temporary',
    'new',
    'old',
    'backup',
    'main',
    'primary',
    'secondary',
    'first',
    'last',
    'start',
    'end',
    'begin',
    'finish',
    'complete',
    'done',
    'ready',
    'go',
    'stop',
    'pause',
    'play',
    'run',
    'walk',
    'jump',
    'fly',
    'swim',
    'drive',
    'ride',
    'sit',
    'stand',
    'sleep',
    'wake',
    'eat',
    'drink',
    'work',
    'play',
    'study',
    'learn',
    'teach',
    'help',
    'save',
    'load',
    'open',
    'close',
    'lock',
    'unlock',
    'on',
    'off',
    'yes',
    'no',
    'true',
    'false',
    'good',
    'bad',
    'big',
    'small',
    'hot',
    'cold',
    'fast',
    'slow',
    'high',
    'low',
    'up',
    'down',
    'left',
    'right',
    'in',
    'out',
    'here',
    'there',
    'now',
    'then',
    'today',
    'tomorrow',
    'yesterday'
]

def try_password(password):
    """Try a password against the hash"""
    try:
        return check_password_hash(target_hash, password)
    except Exception as e:
        print(f"Error checking password '{password}': {e}")
        return False

def main():
    print("Attempting to crack PBKDF2 password hash...")
    print(f"Target hash: {target_hash}")
    print("=" * 60)
    
    # Try common passwords
    print("Trying common passwords...")
    for password in common_passwords:
        print(f"Trying: {password}")
        if try_password(password):
            print(f"\n🎉 PASSWORD FOUND: {password}")
            return
    
    print("\nCommon passwords failed. Trying variations...")
    
    # Try variations with numbers
    base_words = ['admin', 'hoa', 'duong', 'hoahuongduong', 'password']
    for word in base_words:
        for i in range(10):
            variations = [
                f"{word}{i}",
                f"{word}0{i}",
                f"{word}{i}{i}",
                f"{word}123{i}",
                f"{i}{word}",
                f"{word}{i}23",
                f"{word}20{i}",
                f"{word}202{i}"
            ]
            
            for variation in variations:
                print(f"Trying: {variation}")
                if try_password(variation):
                    print(f"\n🎉 PASSWORD FOUND: {variation}")
                    return
    
    # Try simple brute force for short passwords (4 chars)
    print("\nTrying 4-character brute force (numbers only)...")
    for password in itertools.product('0123456789', repeat=4):
        password_str = ''.join(password)
        print(f"Trying: {password_str}")
        if try_password(password_str):
            print(f"\n🎉 PASSWORD FOUND: {password_str}")
            return
    
    print("\n❌ Password not found with current methods.")
    print("You may need to:")
    print("1. Try more specific passwords related to your application")
    print("2. Use a more powerful password cracking tool like hashcat")
    print("3. Reset the password in the database directly")

if __name__ == "__main__":
    main()
