import argparse
import itertools
from multiprocessing import Pool
from zipfile import ZipFile

dictionary_file = 'dictionary.txt'
class PasswordCracker:
    def __init__(self, zip_file):
        self.matched_password = None
        self.zip_file = zip_file
        self.total_passwords = 0

    def generate_passwords(self, min_length, max_length, character_set):
        passwords = []
        for length in range(min_length, max_length + 1):
            for combination in itertools.product(character_set, repeat=length):
                password = ''.join(combination)
                passwords.append(password)
        return passwords

    def crack_passwords_with_brute_force(self, min_length, max_length, character_set):
        passwords = self.generate_passwords(min_length, max_length, character_set)
        for password in passwords: 
            self.total_passwords += 1
            try:
                with ZipFile(self.zip_file) as zipObj:
                    zipObj.extractall(pwd=bytes(password, 'utf-8'))
                    self.matched_password = password
                    break
            except RuntimeError as e:
                continue
    
    def crack_passwords_with_dictionary(self):
        with open(dictionary_file, 'r', encoding="latin-1") as dictionary:
            passwords = dictionary.read().splitlines()
            for password in passwords:
                self.total_passwords += 1
                try:
                    with ZipFile(self.zip_file) as zipObj:
                        zipObj.extractall(pwd=bytes(password, 'utf-8'))
                        self.matched_password = password
                        break
                except RuntimeError as e:
                    continue

    def print_statistics(self):
        print(f"Total Number of Passwords Tried: {self.total_passwords}")
        if self.matched_password:
            print(f"Password Cracked! Password: {self.matched_password}")
        else:
            print("Password Failed.")


def main():
    parser = argparse.ArgumentParser(description='Password cracking tool of Dang Nguyen')
    parser.add_argument('-b', '--brute-force', action='store_true', help='A brute force attack')
    parser.add_argument('--min-length', type=int, default=1, help='Minimum password length for brute force attack')
    parser.add_argument('--max-length', type=int, default=6, help='Maximum password length for brute force attack')
    parser.add_argument('--character-set', default='abcdefghijklmnopqrstuvwxyz0123456789',
                        help='Character set for brute force attack')
    parser.add_argument('--zipfile', type=str, help = 'Zip file to crack')

    args = parser.parse_args()
    cracker = PasswordCracker(args.zipfile)
    if(args.brute_force):
        cracker.crack_passwords_with_brute_force(args.min_length, args.max_length, args.character_set)
    else:
        cracker.crack_passwords_with_dictionary()

    cracker.print_statistics()

if __name__ == '__main__':
    main()