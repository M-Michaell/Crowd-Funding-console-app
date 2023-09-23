import re
from getpass import getpass
import logging
from os import system
import sqlite3 as sql
from database import DatabaseManager
import hashlib
from os import system

class User:
    def __init__(self, first_name, last_name, email, password, mobile_phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.mobile_phone = mobile_phone

class Authentication:
    @staticmethod
    def valid_name(name):
        while True:
            if re.match(r"^[A-Za-z '-]+$", name):
                return name.capitalize()
            else:
                name = input("Not valid! Please enter a valid name: ")

    @staticmethod
    def valid_email(email):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        while True:
            if re.match(email_pattern, email):
                return email
            else:
                email = input("Not valid! Please enter a valid email: ")

    @staticmethod
    def valid_phone(phone):
        mobile_pattern = r"^(012|010|015|011)\d{8}$"
        while True:
            if re.match(mobile_pattern, phone):
                return phone
            else:
                phone = input("Not valid! Please enter a valid phone number: ")

    @staticmethod
    def create_password():
        valid_password = Authentication.valid_password()
        Authentication.confirm_password(valid_password)
        return hashlib.sha256(valid_password.encode()).hexdigest()

    @staticmethod
    def valid_password():
        while True:
            password = getpass("Please enter your password: ")
            letters = r"(?=.*[a-z])(?=.*[A-Z])"
            special_chars = r"[@#$%^&*-_+=<>?/]"
            
            if len(password) < 8:
                print("Not a valid password. Your password must be at least 8 characters, try again.")
            elif not re.search(letters, password):
                print("Invalid password. Your password must contain at least one capital letter and one small letter, try again.")
            elif not any(char in special_chars for char in password):
                print("Invalid password. Your password must contain at least one special character, try again.")
                print("You can pick one of the following: @ # $ % ^ & * - _ + = < > ? /")
            else:
                break
        return password

    @staticmethod
    def confirm_password(password):
        while True:
            confirm_password=getpass("Please retype your password: ")
            if confirm_password == password:
                return
            else:
                print("Confirm password does not match the password")
                while True:
                    reply = input("Press C to confirm it again or press R to reset it: ").lower()
                    if reply == "c":
                        break
                    elif reply == "r":
                        password = Authentication.create_password()
                        break
                    else:
                        print("Invalid choice")

    @staticmethod
    def register_user():
        first_name = input("Please enter your first name: ")
        first_name = Authentication.valid_name(first_name)

        last_name = input("Please enter your last name: ")
        last_name = Authentication.valid_name(last_name)

        email = input("Please enter your email: ").strip().lower()
        email = Authentication.valid_email(email)

        password = Authentication.create_password()

        mobile_phone = input("Please enter your mobile phone: ")
        mobile_phone = Authentication.valid_phone(mobile_phone)

        return User(first_name, last_name, email, password, mobile_phone)

    @staticmethod
    def login_user(db_manager):
        email = input("Please enter your email address: ").strip().lower()

        try:
            with sql.connect(db_manager.db_name) as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM users WHERE email=?", (email,))
                user = cursor.fetchone()
                while True:
                    if user:
                        input_password = getpass("Please enter your password: ")
                        password=hashlib.sha256(input_password.encode()).hexdigest()
                        stored_password = user[3]

                        if password == stored_password:
                            system("clear")
                            print("Login successful!")
                            print(f"\t Welcome back {user[0]}")
                            return email
                        else:
                            print("Incorrect password. Please try again.")
                    else:
                        print("Email not found. Please register before logging in.")
                        break

        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            return False
