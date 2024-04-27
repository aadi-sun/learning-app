import random
import string

def generate_random_code(length):
    characters = string.ascii_letters + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code

# Generate a 6-character random code
random_code = generate_random_code(15)
print("Your random code for online learning:", random_code)
