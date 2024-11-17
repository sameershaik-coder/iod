import random
import string

def generate_invalid_text():
    return "~`!@#$%^&*()_+{}|:\"<>?,./;'[]\\-="+generate_random_text(5)

def generate_random_text(length):
    letters = string.ascii_letters  # includes both uppercase and lowercase letters
    random_text = ''.join(random.choice(letters) for _ in range(length))
    return random_text

def generate_random_number(min_value, max_value):
    return random.randint(min_value, max_value)

def generate_random_email():
    # Define the domain and extension of the email
    domain = "example"
    extension = "com"

    # Generate a random string for the username
    length = random.randint(5, 10)  # Choose a random length for the username
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    # Combine the username, domain, and extension to create the email
    email = f"{username}@{domain}.{extension}"

    return email
