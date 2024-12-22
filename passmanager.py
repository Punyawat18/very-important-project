import json
import os
import base64
import keyboard
import time


class Profile:

    def __init__(self, Profile, Password):
        self.profile = Profile
        try:
            os.makedirs(f'{os.path.dirname(__file__)}/password-data/{self.profile}')
            with open(f'{os.path.dirname(__file__)}/password-data/{self.profile}/Profilepass.txt', 'x') as file:
                file.write(str(Password.encode("utf-8")))
        except FileExistsError:
            Verify_password = input("Please enter Profile password for verification: ")
            with open(f'{os.path.dirname(__file__)}/password-data/{self.profile}/Profilepass.txt', 'r') as file:
                self.Password = file.readline()
                # To prevent random guessing by make it harder(each wrong guess need to restart whole program)
                assert str(Verify_password.encode("utf-8")) == self.Password, (
                    "Verification fail wrong password Terminate the program"
                )


class App(Profile):

    def __init__(self, Profile, ProfilePass, Appname):
        super().__init__(Profile, ProfilePass)
        self.name = Appname
        try:
            os.makedirs(f'{os.path.dirname(__file__)}/password-data/{Profile}/{self.name}', exist_ok=True)
        except FileExistsError:
            pass

class Account(App):

    def __init__(self, Profile, ProfilePass, Appname, Username, Password):
        super().__init__(Profile, ProfilePass, Appname)
        self.username = Username
        self.password = Password
        try:
            with open(f'{os.path.dirname(__file__)}/password-data/{Profile}/{Appname}/{self.username}.json', 'x') as file:
                file.write(self.encoding())
                self.Showpassword = self.password
        except FileExistsError:
            with open(f'{os.path.dirname(__file__)}/password-data/{Profile}/{Appname}/{self.username}.json', 'r') as file:
                self.Encoded = file.read()
                self.Showpassword = self.decoding()

    def encoding(self):
        EncodeKey = len(self.password) + 4
        PassAscii = [ord(_) for _ in self.password]
        EncodedPassword1 = list(map(lambda x : x + EncodeKey, PassAscii))
        EncodedPassword2 = list(
            map(lambda x : str(x).encode('utf-16'), EncodedPassword1)
        )
        EncodedPassword3 = [base64.b64encode(_).decode('utf-8')
                            for _ in EncodedPassword2]
        return json.dumps(EncodedPassword3)
    
    def decoding(self):
        Encoded3 = json.loads(self.Encoded)
        Encoded2 = [base64.b64decode(_.encode('utf-8')) for _ in Encoded3]
        Encoded1 = [int(x.decode('utf-16')) for x in Encoded2]
        EncodeKey = len(Encoded1) + 4
        PassAscii = [x - EncodeKey for x in Encoded1]
        OriginalPass = ''.join(chr(x) for x in PassAscii)
        return OriginalPass

def Profile_selection():
    while True:
        print("If User choose to create new profile but profile already exist the program will treat it as User Select that profile instead and vice versa")
        print("Create/Select Profile Press C for Create , Press S for Select")
        Profile_mode = keyboard.read_key().lower()
        #just be there so that read key wont affect next real input
        keyboard.press_and_release('enter')
        trash = input()
        if Profile_mode != 'c' and Profile_mode != 's':
            print("Incorrect input accepting only C or S as input")
            time.sleep(1)
        else:
            if Profile_mode == 'c':
                Profile = input("Name for new Profile: ")
                Password = input("Choose Password for new profile(Can not be change once select): ")
                return [Profile, Password]
            else:
                Profile = input(f"Please Select Profile From: , {os.listdir(f'{os.path.dirname(__file__)}/password-data')}: ")
                Password = input("Please enter Profile Password: ")
                return [Profile, Password]

def App_selection(Profile):
    while True:
        print("If User choose to add new app but app already exist the program will treat it as User Select that app instead and vice versa")
        print("Add new App (Press A) or Select Existing App(Press S)")
        keyboard.block_key('enter')
        App_mode = keyboard.read_key().lower()
        keyboard.unblock_key('enter')
        #just be there so that read key wont affect next real input
        keyboard.press_and_release('enter')
        trash = input()
        if App_mode != 'a' and App_mode != 's':
            print("Incorrect input accepting only A or S as input")
            time.sleep(1)
        else:
            if App_mode == 'a':
                App = input("Name for new App: ")
                return App
            else:
                try:
                    App_list = os.listdir(f'{os.path.dirname(__file__)}/password-data/{Profile}')
                    App_list.remove('Profilepass.txt')
                    App = input(f"Please Select App From {App_list}: ")
                    return App
                except FileNotFoundError:
                    App = input(f"Please Select New app name(None exist yet): ")
                    return App
            
def Username_and_Password(Profile, App):
    while True:
        print("If User choose to create new account but account already exist the program will treat it as User Select that account instead and vice versa")
        print("Add new Account (Press A) or Select Existing Account(Press S)")
        keyboard.block_key('enter')
        Account_mode = keyboard.read_key().lower()
        keyboard.unblock_key('enter')
        #just be there so that read key wont affect next real input
        keyboard.press_and_release('enter')
        trash = input()
        if Account_mode != 'a' and Account_mode != 's':
            print("Incorrect input accepting only A or S as input")
            time.sleep(1)
        else:
            if Account_mode == 'a':
                Account = input("Name for new Account: ")
                Password = input("Password for New Account: ")
                return [Account, Password]
            else:
                try:
                    Account_file_list = os.listdir(f'{os.path.dirname(__file__)}/password-data/{Profile}/{App}')
                    Account_list = [os.path.splitext(file)[0]
                                    for file in Account_file_list]
                    Account = input(f"Please Select App From {Account_list}: ")
                    return [Account, None]
                except FileNotFoundError:
                    print("Username does not exist yet")
                    Account = input("Please Choose New username: ")
                    Password = input("Password for New Account: ")
                    return [Account, Password]
        


def main():
    Profile_data = Profile_selection()
    Profile = Profile_data[0]
    assert Profile != "", "error profile name cant be empty"
    Profile_password = Profile_data[1]
    App = App_selection(Profile)
    assert App != "", "error app name cant be empty"
    Account_data = Username_and_Password(Profile, App)
    Account_name = Account_data[0]
    assert Account_name != "", "Username cant be empty"
    Account_password = Account_data[1]
    New_account = Account(Profile=Profile,
                          ProfilePass=Profile_password,
                          Appname=App,
                          Username=Account_name,
                          Password=Account_password)
    print(f"Profile : {New_account.profile}, App : {New_account.name}, [Username : {New_account.username}, Password : {New_account.Showpassword}]")

main()
