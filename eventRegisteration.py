import json
import os
import login

# Dedicated folder
DATA_FOLDER = "JSON Data Folder"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

PARTICIPANTS_FILE = os.path.join(DATA_FOLDER, "participants.json")
EVENTS_FILE = os.path.join(DATA_FOLDER, "events.json")

def load_participants():
    if os.path.exists(PARTICIPANTS_FILE):
        try:
            with open(PARTICIPANTS_FILE, 'r', encoding="utf-8") as file:
                return json.load(file)
        except:
            return []
    return []

def save_participants(participants):
    with open(PARTICIPANTS_FILE, 'w', encoding="utf-8") as file:
        json.dump(participants, file, indent=4)

def load_events(): #adjusted to ensure there is no issue when merging #adjusted by reyao
    if os.path.exists(EVENTS_FILE):
        try:
            with open(EVENTS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

                # Convert event dictionary → list of events
                event_list = []
                for event_id, details in data["events"].items():
                    details["event_id"] = event_id   # add the id inside the dict
                    event_list.append(details)

                return event_list

        except:
            return []
    return []


def check_duplicate(student_id, event_id, participants):
    for participant in participants:
        if participant['student_id'] == student_id and participant['event_id'] == event_id:
            return True
    return False

def get_event_capacity(event_id, events):
    for event in events:
        if event['event_id'] == event_id:
            return event['capacity']
    return None

def count_registered_participants(event_id, participants):
    count = 0
    for participant in participants:
        if participant['event_id'] == event_id:
            count += 1
    return count

def register_participant():
    print("\nPARTICIPANT REGISTRATION")
    
    participants = load_participants()
    events = load_events()
    
    if len(events) == 0:
        print("\nNo events available.")
        input("\nPress Enter to continue...")
        return
    
    print("\nAvailable Events:")
    print("-" * 70)
    print(f"{'ID':<3} {'Title':<23} {'Date':<10} {'Remaining':<10} {'Capacity':<10}")
    print("-" * 70)

    for event in events:
        registered = count_registered_participants(event['event_id'], participants)
        remaining = event['capacity'] - registered

        print(
            f"{event['event_id']:<3}"
            f"{event['title']:<23}"
            f"{event['date']:<14}"
            f"{str(remaining) + '/' + str(event['capacity']):<12}"
            f"{event['capacity']:<10}"
        )

    print("-" * 70)

    
    try:
        event_id = input("\nEnter Event ID: ")
        event_capacity = get_event_capacity(event_id, events)
        if event_capacity is None:
            print("\nError: Event ID not found")
            input("\nPress Enter to continue...")
            return
        
        #Auto fill the details for consistency #Adjusted by Reyao
        name = login.current_user["name"]
        student_id = login.current_user["userId"]
        email = login.current_user["email"]
        
        if check_duplicate(student_id, event_id, participants):
            print("\nYou have already registered for this event.")
            print("Student ID:", student_id)
            print("Event ID:", event_id)
            input("\nPress Enter to continue...")
            return
        
        registered_count = count_registered_participants(event_id, participants)
        if registered_count >= event_capacity:
            print("\nError: Event is full")
            print("Capacity:", event_capacity)
            print("Already Registered:", registered_count)
            input("\nPress Enter to continue...")
            return
        
        new_participant = {
            'name': name,
            'student_id': student_id,
            'email': email,
            'event_id': event_id
        }
        
        participants.append(new_participant)
        save_participants(participants)
        
        print("\nRegistration Successful")
        print("Name:", name)
        print("Student ID:", student_id)
        print("Email:", email)
        print("Event ID:", event_id)
        
    except Exception as e:
        print("\nAn error occurred:", e)
        input("\nPress Enter to continue...")

def view_participants_by_event():
    print("\nVIEW PARTICIPANTS BY EVENT")
    
    participants = load_participants()
    events = load_events()
    
    if len(events) == 0:
        print("\nNo events available")
        input("\nPress Enter to continue...")
        return
    
    if len(participants) == 0:
        print("\nNo participants registered yet")
        input("\nPress Enter to continue...")
        return
    
    print("\nAvailable Events:")
    print("-" * 45)
    print(f"{'ID':<3} {'Title':<22} {'Registered':<10}")
    print("-" * 45)

    for event in events:
        registered = count_registered_participants(event['event_id'], participants)

        print(
            f"{event['event_id']:<5}"
            f"{event['title']:<25}"
            f"{registered:<10}"
        )

    print("-" * 45)

    
    event_id = input("\nEnter Event ID to view participants: ")
    
    event_participants = []
    for participant in participants:
        if participant['event_id'] == event_id:
            event_participants.append(participant)
    
    if len(event_participants) == 0:
        print("\nNo participants found for Event ID:", event_id)
    else:
        print("\nParticipants for Event ID:", event_id)

        # Table header
        print("-" * 75)
        print(f"{'No.':<5}{'Name':<25}{'Student ID':<15}{'Email':<30}")
        print("-" * 75)

        # Rows
        for i, p in enumerate(event_participants, start=1):
            print(f"{i:<5}{p['name']:<25}{p['student_id']:<15}{p['email']:<30}")

        # Total count
        print("-" * 75)
        print(f"Total Participants: {len(event_participants)}")

    
    input("\nPress Enter to continue...")

def registration_menu():
    while True:
        eventList = load_events()

        print("\nAvailable Events")
        print("-" * 80)
        print(f"{'ID':<5}{'Title':<20}{'Date':<12}{'Time':<10}{'Venue':<25}{'Capacity':<10}")
        print("-" * 80)

        for e in eventList:
            print(f"{e['event_id']:<5}{e['title']:<20}{e['date']:<12}{e['time']:<10}{e['venue']:<25}{e['capacity']:<10}")
        print("-" * 80)


        print("\nPARTICIPANT REGISTRATION MENU")
        print("1. Register New Participant")
        print("2. View Participants by Event")
        print("0. Return to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            register_participant()
        elif choice == '2':
            view_participants_by_event()
        elif choice == '0':
            print("\nReturning to main menu...")
            break
        else:
            print("\nInvalid option")
            input("Press Enter to continue...")

if __name__ == "__main__":
    registration_menu()