#PASSWORD GENERATOR MODULE
import random

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def password_generator():
    #no of random letters, numbers, symbol
    nr_letter = random.randint(8,10)
    nr_number = random.randint(8,10)
    nr_symbols = random.randint(8,10)

    #initialising password variable to populate with for loop
    password = [random.choice(letters) for i in range(nr_letter)]
    password += [random.choice(numbers) for i in range(nr_number)]
    password += [random.choice(symbols) for i in range(nr_symbols)]

    #shuffling the password
    random.shuffle(password)

    password = "".join(password)
    return password