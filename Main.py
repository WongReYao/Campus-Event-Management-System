import login
import eventManagement
import registerUser
import utility
import eventRegisteration
import search

exitProgram=False
loginStatus = False
userRole = None


while(exitProgram==False): 
    print("===Welcome to Campus Event Management System===")
    print("Enter your Credentials to Login, Enter 0 to exit.")

    loginStatus,userRole=login.login() #Call the login function then get the status and role

    if userRole=="exit":
        print("\n==========Program Exited==========\n")
        break

    while(loginStatus==True): #If login returned true
        #Provide menu and function based on roles
        if (userRole=="admin"):
            print("\n====== Menu Page ======")
            print("1. Manage Event.")
            print("2. View User List")
            print("3. Create User")
            print("4. Remove User")
            print("0. Back.")
            print("=======================")

        elif (userRole=="lecturer"):
            print("\n====== Menu Page ======")
            print("1. View Event List")
            print("3. Search for Events.") #not working
            print("3. Attendance page.")
            print("0. Back.")
            print("=======================")

        else:
            print("\n====== Menu Page ======")
            print("1. Register for Events.")
            print("2. Search for Events.") #not working
            print("3. View Attendance.") #missing view feedback 
            print("0. Back.")
            print("=======================")

        userInput=input("\nSelect your Destination: ")

        if(userRole=="admin"):
            if(userInput=="1"):
                eventManagement.main()
            elif(userInput=="2"):
                data=registerUser.viewUserList()
                if not data:
                    print("\n=====There is no available user.=====")
                else:
                    print("\n===== Registered Users =====")
                    print(f"{'ID':<10}{'Name':<40}{'Email':<30}{'Role':<10}")
                    print("-" * 90)

                    for user in data:
                        print(f"{user.get('userId',''):<10}{user.get('name',''):<40}{user.get('email',''):<30}{user.get('role',''):<10}")
                    print("-" * 90)

            elif(userInput=="3"):
                registerUser.registerUser()

            elif(userInput=="4"):
                registerUser.removeUser()

            elif(userInput=="0"):
                loginStatus=False
                break

            else:
                print("\n=====Invalid Option.=====")
                input("Enter to Continue")

        elif(userRole=="lecturer"):
            if(userInput=="1"):
                events, next_id = eventManagement.load_events()
                eventManagement.view_events(events)
                
            elif(userInput=="2"):
                search.search_menu()
            elif(userInput=="3"):
                utility.attendance() #need to register student to event first
            elif(userInput=="0"):
                loginStatus=False
                break
            else:
                print("\n=====Invalid Option.=====")
                input("Enter to Continue")

        else:
            if(userInput=="1"):
                #Register for Events
                eventRegisteration.registration_menu()
                
            elif(userInput=="2"):
                search.search_menu()
            elif(userInput=="3"):
                utility.student_view_attendance(login.id)
            elif(userInput=="0"):
                loginStatus=False
                break
            else:
                print("\n=====Invalid Option.=====")            
                input("Enter to Continue")

