'''
random is for randomly choosing the next character in the password
re is for regular expression used in the complexity checker
string is for inputting the appropriate characters into the generator character pool
'''
import random
import re
import string

def generate_password(length=14, use_upper=True, use_lower=True, use_num=True, use_special=True):
    '''
    Generates password based on selected arguments, default is to CIS standard
    '''
    if not any([use_upper, use_lower, use_num, use_special]):
        print("Error: At least one character type must be selected")
        return None

    # Ensure the password contains at least one of each selected character type
    password_chars = []
    char_pool = ''

    if use_upper:
        char_pool += string.ascii_uppercase
        password_chars.append(random.choice(string.ascii_uppercase))
    if use_lower:
        char_pool += string.ascii_lowercase
        password_chars.append(random.choice(string.ascii_lowercase))
    if use_num:
        char_pool += string.digits
        password_chars.append(random.choice(string.digits))
    if use_special:
        char_pool += string.punctuation
        password_chars.append(random.choice(string.punctuation))

    # Fill the rest of the password length with random characters from the pool
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(random.choice(char_pool))

    # Shuffle the list to ensure randomness and join to form the password string
    random.shuffle(password_chars)
    password = ''.join(password_chars)

    return password

def check_password_strength(password):
    '''Verifies password complexity to CIS standard'''
    score = 0
    feedback = []

    # Length check
    if len(password) >= 14:
        score += 2
        feedback.append("Excellent length (14+ characters).")
    elif len(password) >= 8:
        score += 1
        feedback.append("Good length (8-13 characters).")
    else:
        feedback.append("Weak: Password should be at least 8 characters long.")

    # Character type checks
    if re.search(r'[A-Z]', password):
        score += 1
        feedback.append("Contains uppercase letters.")
    else:
        feedback.append("Suggestion: Add uppercase letters for more strength.")

    if re.search(r'[a-z]', password):
        score += 1
        feedback.append("Contains lowercase letters.")
    else:
        feedback.append("Suggestion: Add lowercase letters for more strength.")

    if re.search(r'[0-9]', password):
        score += 1
        feedback.append("Contains digits.")
    else:
        feedback.append("Suggestion: Add digits for more strength.")

    if re.search(r'[^A-Za-z0-9]', password):
        score += 1
        feedback.append("Contains special characters.")
    else:
        feedback.append("Suggestion: Add special characters (e.g., !@#$) for more strength.")

    # Determine strength level based on the score
    if score >= 6:
        strength = "Very Strong"
    elif score >= 4:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    return {"strength": strength, "score": score, "feedback": feedback}

def main_menu():
    """Displays the main menu and handles user interaction"""
    while True:
        print("\n--- Password Tool Menu ---")
        print("1. Generate a new secure password")
        print("2. Check the strength of your password")
        print("3. Exit")
        choice = input("Please enter your choice (1, 2, or 3): ")

        if choice == '1':
            # Generate a new password and check its strength
            new_password = generate_password()
            if new_password:
                print(f"\nGenerated Password: {new_password}")
                strength_report = check_password_strength(new_password)
                print(f"Password Strength: {strength_report['strength']}")
                print(f"Score: {strength_report['score']}/6")
                print("Analysis:")
                for item in strength_report['feedback']:
                    print(f"- {item}")

        elif choice == '2':
            # Check the strength of a user-provided password
            custom_password = input("\nEnter the password you want to check: ")
            strength_report = check_password_strength(custom_password)
            print(f"\nPassword Strength: {strength_report['strength']}")
            print(f"Score: {strength_report['score']}/6")
            print("Analysis:")
            for item in strength_report['feedback']:
                print(f"- {item}")

        elif choice == '3':
            # Exit the program
            print("Closing Application")
            break

        else:
            # Handle invalid input
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main_menu()
