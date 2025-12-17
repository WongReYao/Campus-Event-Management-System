import json
import os

#Declare variable used
userId = None
role = None
name = None
email=None
password=None

#view available user
# Define the folder
DATA_FOLDER = "JSON Data Folder"

# Ensure the folder exists
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

#create a path to the file
FILE = os.path.join(DATA_FOLDER, "userList.json")

#Start of view user list function
def viewUserList(fileName=FILE):
    # Create the file if it doesn't exist
    if not os.path.exists(fileName):
        with open(fileName, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Read and return the data
    with open(fileName, "r",encoding="utf-8") as f:
        data = json.load(f)

    return data
#End of view user list function


#Add user
#Start of register user function
def registerUser(filename=FILE):

    userId=input("Insert assigned ID: ") #need to make sure id is unique
    role=input("Insert assigned role (Student/Lecturer): ").lower()
    name=input("Insert user name: ")
    email=input("Insert user email: ")
    password=input("Insert assigned password: ")

    data=viewUserList()

    #Create a new user
    newUser={ #User will have an id,name,email,role
        "userId": userId,
        "role": role,
        "name": name,
        "email": email,
        "password": password
    }

    data.append(newUser) #Add the user after the available data

    #Write the data into the file
    with open(filename, "w",encoding="utf-8") as f:
        json.dump(data, f ,indent=4)

    print("User Created Successfully")
#End of register user function

#Delete user
#Start of delete user function
def removeUser(filename=FILE):
    data=viewUserList() #Get the available user list

    #Check availability of user in the data
    if not data:
        print("===== No available User =====")
    else:
        print("\n===== Registered Users =====")
        print(f"{'ID':<10}{'Name':<40}{'Email':<30}{'Role':<10}")
        print("-" * 90)

        for user in data:
            print(f"{user.get('userId',''):<10}{user.get('name',''):<40}{user.get('email',''):<30}{user.get('role',''):<10}")
        print("-" * 90)

    userId=input("Insert ID that want to be removed: ") #prompt user again on if he is sure he want to delete the user

    
    #If the user id is available in the system then delete
    if any(user["userId"] == userId for user in data):
        while True:
            #Check confirmation from user
            confirmation = input("Are you sure you want to delete the user? (Y/N):").lower()
            if confirmation=="y":
                data= [user for user in data if user["userId"]!=userId]
                with open(filename, "w",encoding="utf-8") as f:
                    json.dump(data,f,indent=4)
                print("Data removed")
                break
            elif confirmation=="n":
                print("Data removal aborted.")
                break
            else:
                print("Invalid input")

    else:
        print("Unavailable/Invalid input.")
