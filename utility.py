import json
import os
import eventManagement
import eventRegisteration
import csv


#Start of feedback function
#Feedback function with 3 parameter
# Dedicated folder
DATA_FOLDER = "JSON Data Folder"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

FEEDBACK_FILE = os.path.join(DATA_FOLDER, "feedback.json")
ATTENDANCE_FILE = os.path.join(DATA_FOLDER, "attendance.json")

ATTENDANCE_FOLDER = "Attendance Folder"

if not os.path.exists(ATTENDANCE_FOLDER):
    os.makedirs(ATTENDANCE_FOLDER)

def feedback(event_id, student_id, rating, feedback_text, filename=FEEDBACK_FILE):
    # Create file if not exist
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Load existing feedback
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Create new feedback entry
    new_feedback = {
        "event_id": event_id,
        "student_id": student_id,
        "rating": rating,
        "feedback": feedback_text
    }

    data.append(new_feedback)

    # Save
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\nThank you! Your rating ({rating}) and feedback have been submitted.\n")

#End of feedback


def averageRating(event_id, filename=FEEDBACK_FILE):
    with open(filename, "r") as f:
        data = json.load(f)

    event_ratings = [
    item["rating"] 
    for item in data 
    if item.get("event_id") == event_id
    ]


    if event_ratings:
        avg = sum(event_ratings) / len(event_ratings)
        print(f"Average Rating for Event {event_id}: {avg:.2f}")
    else:
        print("No ratings for this event yet.")


def displayComment(event_id, filename=FEEDBACK_FILE): #Did not find an appropriate place to include this function
    with open(filename, "r") as f:
        data = json.load(f)

    comments = [item["feedback"] for item in data if item["event_id"] == event_id]

    if not comments:
        print("No feedback comments yet.")
        return

    print("\nFeedback Comments:")
    for c in comments:
        print(f"- {c}")


def student_view_attendance(student_id):
    events, _ = eventManagement.load_events()
    participants = eventRegisteration.load_participants()
    attendance_list = load_attendance()

    print(f"\n===== Attendance Summary for Student {student_id} =====\n")

    student_events = [p for p in participants if p["student_id"] == student_id]

    if not student_events:
        print("You have not registered for any events.")
        return

    # Display all attended events
    # Print header
    print("\n" + "-"*50)
    print(f"{'Event ID':^10} | {'Event Name':^25} | {'Attendance':^15}")
    print("-"*50)

    # Print each student event
    for reg in student_events:
        event_id = reg["event_id"]
        title = events.get(int(event_id), {}).get("title", "Unknown Event")

        record = next(
            (a for a in attendance_list
            if a["event_id"] == event_id and a["student_id"] == student_id),
            None
        )

        status = record["status"] if record else "Not Marked Yet"

        # Center-align each column
        print(f"{event_id:^10} | {title:^25} | {status:^15}")

    print("-"*50)


    # Ask for feedback
    give = input("\nWould you like to provide feedback for an event? (Y/N): ").lower()

    if give == "y":
        event_id = input("Enter the Event ID you want to rate: ")

        rating = int(input("Enter rating (1–5): "))
        feedback_text = input("Enter your feedback: ")

        feedback(event_id, student_id, rating, feedback_text)
        averageRating(event_id)


def attendance():
    while True:
        print("\n===== Attendance Menu =====")
        print("1. Select Event for Attendance Taking")
        print("2. View Attendance for an Event")
        print("0. Back")

        choice = input("Choose: ")

        if choice == "1":
            take_attendance()
        elif choice == "2":
            view_attendance()
        elif choice == "0":
            break
        else:
            print("Invalid Input")

def take_attendance():
    events, _ = eventManagement.load_events()        
    participants = eventRegisteration.load_participants()

    if not events:
        print("\nNo events available.")
        return

    print("\nAvailable Events:")
    for event_id, event in events.items():
        print(f"{event_id} - {event['title']}")

    event_id = input("\nEnter event ID to take attendance: ")

    if int(event_id) not in events:
        print("Invalid event ID.")
        return

    # Get registered students
    registered_students = [p for p in participants if p["event_id"] == event_id]
    if not registered_students:
        print("\nNo students registered for this event.")
        return

    # Load existing attendance
    attendance_list = load_attendance()

    print("\nMark attendance (P = Present, A = Absent):")
    for student in registered_students:
        print(f"\nStudent: {student['student_id']} - {student['name']}")
        status_input = input("Present (P) / Absent (A): ").lower()
        status = "Present" if status_input == "p" else "Absent"

        # Replace existing record if exists
        record_found = False
        for record in attendance_list:
            if record["event_id"] == event_id and record["student_id"] == student["student_id"]:
                record["status"] = status
                record_found = True
                break
        if not record_found:
            attendance_list.append({
                "event_id": event_id,
                "student_id": student["student_id"],
                "name": student["name"],
                "status": status
            })

    save_attendance(attendance_list)
    print("\nAttendance saved successfully.")


def view_attendance():
    attendance_list = load_attendance()
    events, _ = eventManagement.load_events()

    if not events:
        print("\nNo events available.")
        return

    print("\nAvailable Events:")
    for event_id, event in events.items():
        print(f"{event_id} - {event['title']}")

    selected_id = input("\nEnter Event ID to view attendance: ")
    if int(selected_id) not in events:
        print("Invalid event ID.")
        return

    # Filter attendance for that event
    event_attendance = [a for a in attendance_list if a["event_id"] == selected_id]

    if not event_attendance:
        print("\nNo attendance records found for this event.")
        return

    print(f"\nAttendance for Event '{events[int(selected_id)]['title']}':")
    total = len(event_attendance)
    present = sum(1 for a in event_attendance if a["status"] == "Present")
    absent = sum(1 for a in event_attendance if a["status"] == "Absent")

    print(f"Total Students: {total} | Present: {present} | Absent: {absent}\n")

    participants = eventRegisteration.load_participants()

    # Fill in missing names
    for record in event_attendance:
        if "name" not in record or not record["name"]:
            for p in participants:
                if p["student_id"] == record["student_id"] and p["event_id"] == record["event_id"]:
                    record["name"] = p["name"]
                    break

    # Print header
    print("-"*60)
    print(f"{'Student ID':^15} | {'Name':^25} | {'Status':^12}")
    print("-"*60)

    # Print each attendance record in tabular form
    for record in event_attendance:
        student_name = record.get("name", "")
        print(f"{record['student_id']:^15} | {student_name:^25} | {record['status']:^12}")

    print("-"*60)

    # Ask if user wants to export CSV
    export = input("\nDo you want to export this attendance to CSV? (Y/N): ").lower()
    if export == "y":
        export_attendance_csv(selected_id, event_attendance, events[int(selected_id)]["title"])



def load_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        return []

    with open(ATTENDANCE_FILE, "r",encoding="utf-8") as f:
        return json.load(f)

def save_attendance(attendance_list):
    with open(ATTENDANCE_FILE, "w",encoding="utf-8") as f:
        json.dump(attendance_list, f, indent=4)


def export_attendance_csv(event_id, event_attendance, event_title):
    filename = f"Attendance_Event_id-{event_id}_{event_title}.csv"
    filepath = os.path.join(ATTENDANCE_FOLDER, filename)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f: #newline="" removes the gap when enter data
        writer = csv.writer(f)

        # Header
        writer.writerow(["Student ID", "Name", "Status"])

        # Rows
        for record in event_attendance:
            writer.writerow([
                record.get("student_id", ""),
                record.get("name", ""),
                record.get("status", "")
            ])

    print(f"Attendance exported to {filepath}")





