import user
import project

def main():
    db_manager = user.DatabaseManager("project.db")
    db_manager.create_user_table()
    db_manager.create_project_table()
    while True:
        print("""
                Welcome !
            
            press (1) for login
            press (2) for sign up
            press (3) for quit
            
            """)

        answer = input("Enter your choice: ")
        if answer == "1":
            email = user.Authentication.login_user(db_manager)
            if email:
                project.General.main_operation(email, db_manager)
        elif answer == "2":
            new_user = user.Authentication.register_user()
            if db_manager.insert_user(new_user):
                print("Registration successful!")
            else:
                print("Registration failed. Please try again.")
        elif answer == "3":
            break
        else:
            print("Wrong answer, please try again.")

if __name__ == "__main__":
    main()


# already exsist users 
# email : m@m.com    pass :Mm@18101998
# email : n@n.com    pass :Mm@18101998