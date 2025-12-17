import json
import os
from datetime import datetime, timedelta


# Dedicated folder for JSON files
DATA_FOLDER = "JSON Data Folder"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

FILE = os.path.join(DATA_FOLDER, "events.json")

#Start of load events function
def load_events():
    try:
        with open(FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        events_dict = data.get("events", {})
        events_list = []

        for event_id, details in events_dict.items():
            details["event_id"] = event_id
            events_list.append(details)

        return events_list

    except FileNotFoundError:
        return []
#End of load events function

#Start of search events with name function
def search_by_name():
    """Search for events by name/title"""
    events = load_events()
    
    if len(events) == 0:
        print("No events available to search.")
        return
    
    search_term = input("Enter event name to search: ").lower()
    
    found_events = []
    for event in events:
        if search_term in event['title'].lower():
            found_events.append(event)
    
    if len(found_events) == 0:
        print(f"No events found with name containing '{search_term}'")
    else:
        print(f"\nFound {len(found_events)} event(s):")
        print(f"{'ID':<3} {'Title':<25} {'Date':<10} {'Time':<8} {'Venue':<20} {'Capacity':<15} {'Description':<30}")
        print("-" * 110)

        for event in found_events:
            print(
                f"{event['event_id']:<5}"
                f"{event['title']:<25}"
                f"{event['date']:<12}"
                f"{event['time']:<8}"
                f"{event['venue']:<20}"
                f"{event['capacity']:<15}"
                f"{event['description']:<30}"
            )

        print("-" * 110)
#End of search events with name function


#Start of search events with date function
def search_by_date():
    """Search for events by date"""
    events = load_events()
    
    if len(events) == 0:
        print("No events available to search.")
        return
    
    search_date = input("Enter date to search (YYYY-MM-DD): ")
    
    # check if date format is correct
    try:
        datetime.strptime(search_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return
    
    found_events = []
    for event in events:
        if event['date'] == search_date:
            found_events.append(event)
    
    if len(found_events) == 0:
        print(f"No events found on {search_date}")
    else:
        print(f"\nFound {len(found_events)} event(s) on {search_date}:")
        print(f"{'ID':<3} {'Title':<25} {'Time':<8} {'Venue':<20} {'Capacity':<15} {'Description':<30}")
        print("-" * 100)

        for event in found_events:
            print(
                f"{event['event_id']:<5}"
                f"{event['title']:<25}"
                f"{event['time']:<8}"
                f"{event['venue']:<20}"
                f"{event['capacity']:<15}"
                f"{event['description']:<30}"
            )

        print("-" * 100)
#End of search events with date function

#Start of search events with capacity function
def filter_by_capacity():
    """Filter events by remaining capacity"""
    events = load_events()
    
    if len(events) == 0:
        print("No events available to filter.")
        return
    
    try:
        min_capacity = int(input("Enter minimum remaining capacity: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    
    # for now we assume capacity is the total capacity
    # later when registration is done, we need to calculate remaining capacity
    filtered_events = []
    for event in events:
        if event['capacity'] >= min_capacity:
            filtered_events.append(event)
    
    if len(filtered_events) == 0:
        print(f"No events found with capacity >= {min_capacity}")
    else:
        print(f"\nFound {len(filtered_events)} event(s) with capacity >= {min_capacity}:")
        print("-" * 100)
        print(f"{'ID':<3} {'Title':<25} {'Date':<12} {'Time':<8} {'Venue':<20} {'Capacity':<15} {'Description':<30}")
        print("-" * 100)

        for event in filtered_events:
            print(
                f"{event['event_id']:<5}"
                f"{event['title']:<25}"
                f"{event['date']:<12}"
                f"{event['time']:<8}"
                f"{event['venue']:<20}"
                f"{event['capacity']:<15}"
                f"{event['description']:<30}"
            )

        print("-" * 100)
#End of search events with capacity function


#Start of search events with days function
def filter_by_days():
    """Filter events happening within X days from today"""
    events = load_events()
    
    if len(events) == 0:
        print("No events available to filter.")
        return
    
    try:
        days = int(input("Enter number of days: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    
    if days < 0:
        print("Number of days must be positive.")
        return
    
    # get today's date
    today = datetime.now().date()
    future_date = today + timedelta(days=days)
    
    upcoming_events = []
    for event in events:
        try:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
            # check if event is between today and future date
            if today <= event_date <= future_date:
                upcoming_events.append(event)
        except ValueError:
            continue
    
    if len(upcoming_events) == 0:
        print(f"No events found within the next {days} day(s)")
    else:
        print(f"\nFound {len(upcoming_events)} event(s) within the next {days} day(s):")
        print("-" * 100)
        print(f"{'ID':<3} {'Title':<25} {'Date':<12} {'Time':<8} {'Venue':<20} {'Capacity':<15} {'Description':<30}")
        print("-" * 100)

        for event in upcoming_events:
            print(
                f"{event['event_id']:<5}"
                f"{event['title']:<25}"
                f"{event['date']:<12}"
                f"{event['time']:<8}"
                f"{event['venue']:<20}"
                f"{event['capacity']:<15}"
                f"{event['description']:<30}"
            )

        print("-" * 100)
#Start of search events with days function


#Start of search menu function
def search_menu():
    """Display search and filter menu"""
    while True:
        print("\n=== Search & Filter Events ===")
        print("1. Search by event name")
        print("2. Search by date")
        print("3. Filter by capacity")
        print("4. Filter by upcoming days")
        print("0. Back")
        print("==============================")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            search_by_name()
        elif choice == '2':
            search_by_date()
        elif choice == '3':
            filter_by_capacity()
        elif choice == '4':
            filter_by_days()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")
#End of search menu function

# test the functions if this file is run directly
if __name__ == "__main__":
    search_menu()