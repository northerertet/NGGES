import unittest
import re
import string
import random

# --- Functions from the main program to be tested ---

def generate_password(args):
    """
    Generates a single random password. This function is designed to be
    called by a parallel process or directly for single generation.
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
    # Handle cases where length might be smaller than the number of character types
    if remaining_length < 0:
        random.shuffle(password_chars)
        return ''.join(password_chars[:length])

    for _ in range(remaining_length):
        password_chars.append(random.choice(char_pool))
        
    random.shuffle(password_chars)
    return ''.join(password_chars)

def check_password_strength(password):
    """
    Checks the strength of a single password. This function is designed to be
    called by a parallel process or directly.
    """
    if not password: # Handle empty or None password
        return (password, "Very Weak", 0)

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

# --- Unit Test Suite ---

class TestPasswordTool(unittest.TestCase):

    def test_generate_password_length(self):
        """Test if the generated password has the correct length."""
        args = (15, True, True, True, True)
        password = generate_password(args)
        self.assertEqual(len(password), 15)

    def test_generate_password_contains_uppercase(self):
        """Test if the generated password contains an uppercase letter."""
        args = (12, True, False, False, False)
        password = generate_password(args)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertFalse(any(c.islower() for c in password))

    def test_generate_password_contains_lowercase(self):
        """Test if the generated password contains a lowercase letter."""
        args = (12, False, True, False, False)
        password = generate_password(args)
        self.assertTrue(any(c.islower() for c in password))
        self.assertFalse(any(c.isdigit() for c in password))

    def test_generate_password_contains_digit(self):
        """Test if the generated password contains a digit."""
        args = (12, False, False, True, False)
        password = generate_password(args)
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertFalse(any(c in string.punctuation for c in password))
        
    def test_generate_password_contains_special_char(self):
        """Test if the generated password contains a special character."""
        args = (12, False, False, False, True)
        password = generate_password(args)
        self.assertTrue(any(c in string.punctuation for c in password))
        self.assertFalse(any(c.isupper() for c in password))
        
    def test_generate_password_all_char_types(self):
        """Test if the generated password contains all requested character types."""
        args = (12, True, True, True, True)
        password = generate_password(args)
        self.assertTrue(re.search(r'[A-Z]', password))
        self.assertTrue(re.search(r'[a-z]', password))
        self.assertTrue(re.search(r'[0-9]', password))
        self.assertTrue(re.search(r'[^A-Za-z0-9]', password))

    def test_check_password_very_strong(self):
        """Test a very strong password."""
        _, strength, score = check_password_strength("V3ryStr0ng!P@ssw0rd")
        self.assertEqual(strength, "Very Strong")
        self.assertEqual(score, 6)

    def test_check_password_strong(self):
        """Test a strong password."""
        _, strength, score = check_password_strength("StrongPass1")
        self.assertEqual(strength, "Strong")
        self.assertEqual(score, 4)

    def test_check_password_moderate(self):
        """Test a moderate password."""
        _, strength, score = check_password_strength("pass123")
        self.assertEqual(strength, "Moderate")
        self.assertEqual(score, 3)

    def test_check_password_weak_short(self):
        """Test a weak password (too short)."""
        _, strength, score = check_password_strength("p@ss")
        self.assertEqual(strength, "Weak")
        self.assertEqual(score, 2) # Score 2 for lower and special

    def test_check_password_weak_no_variety(self):
        """Test a weak password (long but no variety)."""
        _, strength, score = check_password_strength("passwordpassword")
        self.assertEqual(strength, "Weak")
        self.assertEqual(score, 2) # Score 2 for length and lower

    def test_check_password_empty(self):
        """Test an empty password string."""
        _, strength, score = check_password_strength("")
        self.assertEqual(strength, "Very Weak")
        self.assertEqual(score, 0)

if __name__ == '__main__':
    # This allows you to run the tests by executing the script directly
    unittest.main(argv=['first-arg-is-ignored'], exit=False)