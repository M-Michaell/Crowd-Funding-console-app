import re

class Authenication():

    # def __init__(self,first_name):
    #     self.first_name.Authenication.__init__(self

    @classmethod
    def valid_name(cls, name):
        while True :
            if  re.match(r"^[A-Za-z '-]+$", name) :
                break
            else :
                name = input("not valid! , please enter a valid name: ")
        return name.capitalize()
    
    @classmethod
    def valid_email(cls, email):
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        while True :
            if re.match(email_pattern , email) :
                break
            else :
                email = input("not valid!, please enter a valid email: ")
        return email
    @classmethod
    def valid_phone(cls, phone):
        mobile_pattern = r"^(012|010|015|011)\d{8}$"
        while True:
            if re.match(mobile_pattern, phone) :
                break
            else :
                phone = input("not valid!, please enter a valid phone Number: ")
        return phone
    


    @classmethod
    def create_password():
        password = input("Please enter your password")
        valid_password=Authenication.valid_password(password)
        confirming = input("retype your password")
        Authenication.confirm_password(valid_password,confirming)

        

    @classmethod
    def valid_password(cls, password):
        while True :
            letters = r"(?=.*[a-z])(?=.*[A-Z])"
            spiecial_chars ="!@#$%^&*-_+=<>?/"
            if len(password) < 8 :
                print("not a valid password , your password must be at least 8 characters")
                password=input("Please enter a valid password")
            elif not re.search(letters, password) :
                print("invalid password, your password must be at least contains one capital letter and one small letter")
                password=input("Please enter a valid password")
            elif not re.search(spiecial_chars, password) :
                print("invalid password, your password must be at least contains one special character")
                print("you can pick one of the following (@,#,$,%,^,=,...etc)")        
                password=input("Please enter a valid password")
            else :
                break
        return password
    
    @classmethod
    def confirm_password(cls, password, confirm_password) :
        while True :
            if confirm_password == password :
                break
            else :
                print("confirm_password is not matching the password")
                while True :
                    reply =input("press C for confirm  it again or press R to reset it ").lower()
                    if reply == "c" :
                        confirm_password=input("retype your password")
                        break
                    elif reply == "r" :
                        Authenication.create_password()
                    else :
                        print("wrong choice")                   


            

    


    



    @classmethod
    def Redistration(cls):
        
        first_name =input("please enter your first name: ")
        Authenication.valid_name(first_name)
        
        second_name =input("please enter your second name: ")
        Authenication.valid_name(second_name)

        email = input("please enter your email: ")
        Authenication.valid_email(email)
        ##password section
        Authenication.create_password()

        



  





        ##password section
        Moblie_phone = input("Please enter your Moblie phone: ")
        Authenication.valid_phone(Moblie_phone)


Authenication.Redistration()


        

        