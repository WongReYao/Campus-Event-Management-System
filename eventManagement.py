import json
import os

# Dedicated folder for storing JSON data
DATA_FOLDER = "JSON Data Folder"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# File path inside the folder
FILE = os.path.join(DATA_FOLDER, "events.json")

#Start of load event function
def load_events():
    #Check if file exist
    if not os.path.exists(FILE):
        return {}, 1
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return {}, 1

    events = {}
    for k, v in data.get("events", {}).items():
        try:
            events[int(k)] = v
        except:
            pass

    next_id = data.get("next_id", max(events.keys(), default=0) + 1)
    return events, next_id
#End of load event function

#start of save event function
def save_events(events, next_id):
    data = {
        "events": {str(k): v for k, v in events.items()},
        "next_id": next_id
    }
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
#End of load event function

#start of check date function
def valid_date(date):
    if len(date) != 10: #Checking length of the date
        return False
    parts = date.split("-")
    if len(parts) != 3:
        return False
    y, m, d = parts
    return y.isdigit() and m.isdigit() and d.isdigit()
#End of check date function

#start of check time function
def valid_time(t):
    if len(t) != 5:
        return False
    parts = t.split(":")
    if len(parts) != 2:
        return False
    h, m = parts
    return h.isdigit() and m.isdigit()
#End of check time function

#Start of check vapacity function
def valid_capacity(c):
    return c.isdigit() and int(c) > 0
#End of check vapacity function

#Start of add event function
def add_event(events, next_id):
    print("\n--- ADD A NEW EVENT ---\n")
    
    #Using strip function to remove spacing
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return events, next_id

    date = input("Date (YYYY-MM-DD): ").strip()
    if not valid_date(date):
        print("Invalid date format.")
        return events, next_id

    time = input("Time (HH:MM): ").strip()
    if not valid_time(time):
        print("Invalid time format.")
        return events, next_id

    venue = input("Venue: ").strip()

    capacity = input("Capacity (>0): ").strip()
    if not valid_capacity(capacity):
        print("Invalid capacity.")
        return events, next_id

    description = input("Description: ").strip()

    #Dictionary that contains these detail
    events[next_id] = {
        "title": title,
        "date": date,
        "time": time,
        "venue": venue,
        "capacity": int(capacity),
        "description": description
    }

    print(f"Event added with ID = {next_id}")
    next_id += 1
    save_events(events, next_id)
    return events, next_id
#End of add event function

#Start of view events functions
def view_events(events):
    print("\n" + "--- ALL EVENTS ---".center(85, "-") + "\n")
    if not events:
        print("No events found.\n")
        return

    print(f"{'ID':<5} {'Title':<25} {'Date':<12} {'Time':<6} {'Venue':<20} {'Capacity':<5}")
    print("-" * 85)
    print()
    
    for eid, e in sorted(events.items()):#for index, value. Can be understanded as based on the value, get the specific column of value
        title = e.get("title", "N/A")
        date = e.get("date", "N/A")
        time = e.get("time", "N/A")
        venue = e.get("venue", "N/A")
        capacity = e.get("capacity", "N/A")
        print(f"{eid:<5} {title[:25]:<25} {date:<12} {time:<6} {venue[:20]:<20} {capacity:<5}")

    print("-" * 85)
#End of view events functions

#Start of edit events functions
def edit_event(events):
    if not events:
        print("No events to edit.")
        return events

    view_events(events)
    eid = input("Enter event ID to edit: ").strip()
    if not eid.isdigit() or int(eid) not in events:
        print("Invalid ID.")
        return events

    eid = int(eid)
    event = events[eid]

    print("\nLeave blank to keep current value.")
    new_title = input(f"Title ({event.get('title')}): ").strip()
    if new_title:
        event["title"] = new_title

    new_date = input(f"Date ({event.get('date')}): ").strip()
    if new_date and valid_date(new_date):
        event["date"] = new_date

    new_time = input(f"Time ({event.get('time')}): ").strip()
    if new_time and valid_time(new_time):
        event["time"] = new_time

    new_venue = input(f"Venue ({event.get('venue')}): ").strip()
    if new_venue:
        event["venue"] = new_venue

    new_capacity = input(f"Capacity ({event.get('capacity')}): ").strip()
    if new_capacity and valid_capacity(new_capacity):
        event["capacity"] = int(new_capacity)

    new_desc = input(f"Description ({event.get('description')}): ").strip()
    if new_desc:
        event["description"] = new_desc

    events[eid] = event
    save_events(events, max(events.keys()) + 1)
    print("Event updated successfully.")
    return events
#End of edit events functions

#Start of delete events functions
def delete_event(events):
    if not events:
        print("No events to delete.")
        return events

    view_events(events)
    print()
    eid = input("Enter event ID to delete: ").strip()
    if not eid.isdigit() or int(eid) not in events:
        print("Invalid ID.")
        return events

    confirm = input("Are you sure? (y/n): ").lower()
    if confirm == "y":
        del events[int(eid)]
        save_events(events, max(events.keys(), default=0) + 1)
        print("Event deleted.")
    else:
        print("Deletion cancelled.")

    return events
#End of delete events functions


def main():
    events, next_id = load_events()

    while True:
        print("\n===== EVENT MANAGEMENT =====")
        print()
        print("1. Add Event")
        print("2. View Events")
        print("3. Edit Event")
        print("4. Delete Event")
        print("0. Back")
        print()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            events, next_id = add_event(events, next_id)
        elif choice == "2":
            view_events(events)
        elif choice == "3":
            events = edit_event(events)
        elif choice == "4":
            events = delete_event(events)
        elif choice == "0":
            #print("Thank you!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()