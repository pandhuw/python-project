import passchar
import random

print("Welcome to PyPassword Generator")
nr_letters = int(input("How many letters would you like in your password? "))
nr_numbers = int(input("How many numbers would you like? "))
nr_symbols = int(input("How many symbols would you like? "))

password_list = []
for i in range(1, nr_letters + 1):
    password_list += random.choice(passchar.letters)
for i in range(1, nr_numbers + 1):
    password_list += random.choice(passchar.numbers)
for i in range(1, nr_symbols + 1):
    password_list += random.choice(passchar.symbols)

random.shuffle(password_list)

password = ""
for char in password_list:
    password += char

print(f"Your password is: {password}")

input("")
