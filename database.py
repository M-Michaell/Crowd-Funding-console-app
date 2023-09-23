import sqlite3 as sql
import logging
import datetime
import project

class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_user_table(self):
        with sql.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS users (first_name TEXT, last_name TEXT, email TEXT PRIMARY KEY, password TEXT, mobile_phone TEXT)")
            db.commit()

    def insert_user(self, user):
        try:
            with sql.connect(self.db_name) as db:
                cursor = db.cursor()
                cursor.execute("INSERT INTO users (first_name, last_name, email, password, mobile_phone) VALUES (?, ?, ?, ?, ?)",
                               (user.first_name, user.last_name, user.email, user.password, user.mobile_phone))
                db.commit()
            return True
        except sql.IntegrityError:
            logging.error(f"Email '{user.email}' is already in use.")
            return False
        except Exception as e:
            logging.error(f"Error inserting user into the database: {str(e)}")
            return False
        

    def insert_project(self, project):
        try:
            with sql.connect(self.db_name) as db:
                cursor = db.cursor()
                cursor.execute("INSERT INTO project (email, title, details, target, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)",
                               (project.email, project.title, project.details, project.target, project.start_date, project.end_date))
                db.commit()
            return True
        except sql.IntegrityError:
            logging.error(f"Project with title '{project.title}' already exists for this user.")
            return False
        except Exception as e:
            logging.error(f"Error inserting project into the database: {str(e)}")
            return False

    def create_project_table(self):
        with sql.connect(self.db_name) as db:
            cursor = db.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS project (email TEXT, title TEXT, details TEXT,target intger,start_date DATE, end_date DATE, FOREIGN KEY (email) REFERENCES users(email), PRIMARY KEY (email, title))")
            db.commit()

    def user_projects(self, email):
        try:
            with sql.connect(self.db_name) as db:
                cursor = db.cursor()
                cursor.execute("SELECT title FROM project WHERE email=?", (email,))
                projects = cursor.fetchall()
                return projects
        except Exception as e:
            logging.error(f"Error fetching user projects: {str(e)}")
            return []

    def user_project_details(self, email, title):
        try:
            with sql.connect(self.db_name) as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM project WHERE email=? AND title=?", (email, title))
                project = cursor.fetchone()
                return project
        except Exception as e:
            logging.error(f"Error fetching user project details: {str(e)}")
            return []

    def others_project(self):
        try:
            with sql.connect(self.db_name) as db:
                cursor = db.cursor()
                cursor.execute("SELECT title FROM project")
                projects = cursor.fetchall()
                return projects
        except Exception as e:
            logging.error(f"Error fetching other projects: {str(e)}")
            return []

    def project_details_others(self, title):
        try:
            with sql.connect(self.db_name) as db:
                cursor = db.cursor()
                cursor.execute("SELECT * FROM project WHERE title=?", (title,))
                projects = cursor.fetchall()
                return projects
        except Exception as e:
            logging.error(f"Error fetching project details: {str(e)}")
            return []

    def edit_project(self, email, title, thing, new_value):

        if thing =="end_date" :
            start_date= DatabaseManager.user_project_details(self,email,title)[4]
            start_date=str(start_date)
            while True :
                if thing =="end_date" :
                    if project.General.valid_date(new_value):
                        if datetime.datetime.strptime(new_value, "%d/%m/%Y") < datetime.datetime.strptime(start_date, "%d/%m/%Y"):
                            print(f"you must enter a date which come after start_date: {start_date}")
                            return False
                        else:
                            break
                    else :
                        print("not a valid date , you must enter a date in format: dd/mm/yyyy")
                        return False
                else :
                    break
                
                
        try:

            with sql.connect(self.db_name) as db:
                cursor = db.cursor()
                cursor.execute(f"UPDATE project SET {thing}=? WHERE title=? AND email=?", (new_value, title, email))
                db.commit()
                print("Successfully updated")
                return True
        except Exception as e:
            logging.error(f"Error updating project: {str(e)}")
            return False

    def delete_project(self, email, title):
        try:
            with sql.connect(self.db_name) as db:
                cursor = db.cursor()
                cursor.execute("DELETE FROM project WHERE email=? AND title=?", (email, title))
                db.commit()
                print("Successfully deleted")
                return True
        except Exception as e:
            logging.error(f"Error deleting project: {str(e)}")
            return False
