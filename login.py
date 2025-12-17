import registerUser

#Variable used for the login
id=None
password=None

current_user = None  # global variable to store logged-in user

#Start of Login function
def login():
    #Turn the id and current user as global variable
    global current_user
    global id

    #User input login
    id = input("Insert Student ID: ") 
    #Check if user wants to exit program
    if id=="0":
        return False, "exit" #If yes, return false for login success, then exit for the role.
    
    password = input("Insert Password: ") #prompt user to enter password

    #Call the view user list function to get the availabe user as data
    data = registerUser.viewUserList()

    #Check login credentials
    if id=="admin" and password=="12345": #Check Admin
        print("\n=====Login Successful=====")
        return True, "admin"

    for user in data: #Check for lecturer or student
        if user["userId"] == id and user["password"] == password:
            print("\n=====Login Successful=====")
            
            # Save user id for global usage
            current_user = user
            return True, user["role"]
    
    print("\n=====Invalid ID or Password=====\n")
    return False, None
#End of Login function
