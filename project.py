import user
import datetime
import re
from os import system
class Project:
    def __init__(self, email, title, details, target, start_date, end_date):
        self.email = email
        self.title = title
        self.details = details
        self.target = target
        self.start_date = start_date
        self.end_date = end_date



        # validation on date
class General:
    @staticmethod
    def valid_date(date_string):
        date_pattern = r"^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$"

        if not re.match(date_pattern, date_string):
            return False

        day, month, year = map(int, date_string.split('/'))

        if month < 1 or month > 12:
            return False

        if month in [4, 6, 9, 11]:
            if day < 1 or day > 30:
                return False
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                if day < 1 or day > 29:
                    return False
            else:
                if day < 1 or day > 28:
                    return False
        else:
            if day < 1 or day > 31:
                return False

        return True
    

    # main operation 

    @staticmethod
    def main_operation(email, db_manager):
        print("""
         Press (1) to show your projects
         Press (2) to create your project
         Press (3) to show all projects on database
         Press (4) to log out
        
         """)
        while True:
            answer = input("Enter your choice: ")
            if answer == "1":
                General.show_your_project(email, db_manager)
                General.main_operation(email, db_manager)
                break
            elif answer == "2":
                system("clear")
                print("""
                        creating project
                        """)
                new_project=General.project_data(email)
                if db_manager.insert_project(new_project):
                    system("clear")
                    print("Project creation successful!")
                else:
                    print("Project creation failed. Please try again.")

                General.main_operation(email, db_manager)
                break
            elif answer == "3":
                General.other_project_data(db_manager)
                General.main_operation(email, db_manager)
                break
            elif answer == "4":
                break


            else:
                print("Wrong answer! Try again")


                # your porjects

    @staticmethod
    def show_your_project(email, db_manager):
        while True:
            projects = db_manager.user_projects(email)
            for n, project in enumerate(projects):
                print(f'{n+1}) {project[0]}')
            answer = input("""
                Choose your project number to show or edit or delete or press Q to quit.
                Enter your choice: """).strip().lower()
            if answer == "q":
                return  
            try:
                selected_index = int(answer)-1
                if 0 <= selected_index < len(projects):
                    selected = projects[selected_index][0]
                    break
                else:
                    print(f'{selected_index} is not a valid project number, try again')
            except (IndexError, ValueError):
                print("Invalid input. Please enter a valid number.")

        while True:
            print("""
                Press (1) to show all details
                Press (2) to edit
                Press (3) to delete
                Press (4) to go back to the previous menu 
                """)
            answer = input("Enter your choice: ")
            if answer == "1":
                project_details = db_manager.user_project_details(email, selected)
                if project_details:
                                        print(f"""
                            Email:{project_details[0]}
                            Title:{project_details[1]}
                            Details:{project_details[2]}
                            Target:{project_details[3]}
                            Start_Date:{project_details[4]}
                            End_Date:{project_details[5]}

                            """)
                else:
                    print("Project details not found.")
            elif answer == "2":
                General.edit(email, selected, db_manager)
            elif answer == "3":
                db_manager.delete_project(email, selected)
            elif answer == "4":
                return  
            else:
                print("Invalid choice, try again")

            # data get from user when create project 
    @staticmethod
    def project_data(email):
        title = input("Enter project Title: ")
        details = input("Enter project details: ")
        while True:
            target = input("Enter project target: ")
            try:
                int(target)
                break
            except ValueError:
                print("Not a valid number, try again")

        while True:
            print("""
                Enter start date in form dd/mm/yyyy
                or enter now to set today as the start date
                """)
            start_date = input("Enter your choice: ").strip().lower()
            if start_date == "now":
                start_date = datetime.datetime.now()
                start_date = start_date.strftime('%d/%m/%Y')
                break
            elif General.valid_date(start_date):
                break
            else:
                print("Invalid date, try again")

        while True:
            end_date = input("Enter end date in form dd/mm/yyyy: ")
            if General.valid_date(end_date):
                if datetime.datetime.strptime(end_date, "%d/%m/%Y") < datetime.datetime.strptime(start_date, "%d/%m/%Y"):
                    print("End date must be after start date, try again")
                else:
                    break
            else:
                print("Invalid date format, try again")

        return Project(email, title, details, target, start_date, end_date)


            # to edit data of exist Project
    @staticmethod
    def edit(email, title, db_manager):
        while True:
            print("""
                Press (1) to edit title
                Press (2) to edit details
                Press (3) to edit target
                press (4) to edit end_date
                Press (5) to go back to the previous menu
                """)
            answer = input("Enter your answer: ")
            if answer == "1":
                edit_title = input("Enter the new project title: ")
            
            elif answer == "2":
                edit_detail = input("Enter the new project detail: ")
                db_manager.edit_project(email, title, "details", edit_detail)
            elif answer == "3":
                while True:
                    edit_target = input("Enter the new target: ")
                    try:
                        int(edit_target)
                        db_manager.edit_project(email, title, "target", edit_target)
                        break
                    except ValueError:
                        print("Please enter a valid target, try again")
            elif answer =='4' :
                while True :
                    end_date=input("Enter the end date: ")
                    edit_end_date = db_manager.edit_project(email, title, "end_date", end_date)
                    if edit_end_date:
                        break



            elif answer == "5":
                break

                    # to show others project data
    @staticmethod
    def other_project_data(db_manager):
        while True:
            titles = db_manager.others_project()
            for n, title in enumerate(titles):
                print(f"{n+1}) {title[0]}")

            print("\tEnter project number to show all its data or press q for quit:")
            answer = input("Enter your choice: ").strip().lower()
            if answer == "q":
                break
            try:
                selected_index = int(answer)-1
                if 0 <= selected_index < len(titles):
                    wanted = titles[selected_index][0]
                    wanted_project =db_manager.project_details_others(wanted)[0]
                    print(f"""
                            Email:{ wanted_project[0]}
                            Title:{ wanted_project[1]}
                            Details:{ wanted_project[2]}
                            Target:{ wanted_project[3]}
                            Start_Date:{ wanted_project[4]}
                            End_Date:{ wanted_project[5]}

                            """)
                    # print(db_manager.project_details_others(wanted))
                else:
                    print(f'{selected_index} is not a valid project number, try again')
            except ValueError:
                print("Invalid input. Please enter a valid number.")

