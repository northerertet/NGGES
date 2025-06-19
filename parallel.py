'''
random is for randomly choosing the next character in the password
re is for regular expression used in the complexity checker
string is for inputting the appropriate characters into the generator character pool
'''
import random
import re
import string
import time
from multiprocessing import Pool, cpu_count

def generate_password(args):
    """
    Generates a single random password.
    This function is designed to be called by a parallel process
    """
    length, use_uppercase, use_lowercase, use_digits, use_special_chars = args

    if not any([use_uppercase, use_lowercase, use_digits, use_special_chars]):
        return None

    char_pool = ''
    password_chars = []

    # Ensure at least one of each selected character type is included
    if use_uppercase:
        char_pool += string.ascii_uppercase
        password_chars.append(random.choice(string.ascii_uppercase))
    if use_lowercase:
        char_pool += string.ascii_lowercase
        password_chars.append(random.choice(string.ascii_lowercase))
    if use_digits:
        char_pool += string.digits
        password_chars.append(random.choice(string.digits))
    if use_special_chars:
        char_pool += string.punctuation
        password_chars.append(random.choice(string.punctuation))

    # Fill the rest of the password
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(random.choice(char_pool))

    random.shuffle(password_chars)
    return ''.join(password_chars)

def check_password_strength(password):
    """
    Checks the strength of a single password and returns a report
    This function is designed to be called by a parallel process
    """
    score = 0

    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    # Character type checks
    if re.search(r'[A-Z]', password): score += 1
    if re.search(r'[a-z]', password): score += 1
    if re.search(r'[0-9]', password): score += 1
    if re.search(r'[^A-Za-z0-9]', password): score += 1

    if score >= 6: strength = "Very Strong"
    elif score >= 4: strength = "Strong"
    elif score >= 3: strength = "Moderate"
    else: strength = "Weak"

    return (password, strength, score)

def main_menu():
    """Displays the main menu and handles user interaction"""
    # Use all available CPU cores for parallel processing
    num_processes = cpu_count()
    print(f"--- Welcome to the Parallel Password Tool (using {num_processes} cores) ---")

    while True:
        print("\nMenu:")
        print("1. Generate a list of secure passwords")
        print("2. Check strength of a single password")
        print("3. Check strength of passwords from a file (passwords.txt)")
        print("4. Exit")
        choice = input("Please enter your choice: ")

        if choice == '1':
            try:
                count = int(input("How many passwords to generate? "))
                args = [(12, True, True, True, True)] * count

                start_time = time.time()
                with Pool(num_processes) as p:
                    passwords = p.map(generate_password, args)
                end_time = time.time()

                for pw in passwords:
                    print(f"  - {pw}")
                print(f"\nGenerated {count} passwords in {end_time - start_time:.4f} seconds.")

            except ValueError:
                print("Invalid number. Please enter an integer.")

        elif choice == '2':
            password = input("\nEnter the password to check: ")
            _, strength, score = check_password_strength(password)
            print(f"\nPassword Strength: {strength} (Score: {score}/6)")

        elif choice == '3':
            try:
                # Create a dummy file for demonstration if it doesn't exist
                try:
                    with open("passwords.txt", "x", encoding="utf8") as f:
                        f.write("password\n123456\nPassword123!\n")
                    print("Created a sample 'passwords.txt' file for you.")
                except FileExistsError:
                    pass

                with open("passwords.txt", "r", encoding="utf8") as f:
                    passwords = [line.strip() for line in f]

                print(f"Checking {len(passwords)} passwords from 'passwords.txt'...")
                start_time = time.time()

                # Use a process pool to check passwords in parallel
                with Pool(num_processes) as p:
                    results = p.map(check_password_strength, passwords)

                end_time = time.time()

                for pwd, strength, score in results:
                    print(f"  - Password: {pwd:<20} | Strength: {strength:<12} | Score: {score}/6")
                print(f"\nChecked {len(passwords)} passwords in {end_time - start_time:.4f} seconds.")

            except FileNotFoundError:
                print("Error: 'passwords.txt' not found. Please create it.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == '4':
            print("Exiting the Parallel Password Tool. Stay secure!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    # The __name__ == '__main__' guard is crucial for multiprocessing
    main_menu()
