import json
import os

FILENAME = "jobs.json"

# Load jobs from file
def load_jobs():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            return json.load(file)
    return []

# Save jobs to file
def save_jobs():
    with open(FILENAME, "w") as file:
        json.dump(jobs, file, indent=4)

jobs = load_jobs()

def add_job():
    company = input("Company name: ")
    role = input("Role: ")
    status = input("Status (Applied/Interview/etc): ")

    job = {
        "company": company,
        "role": role,
        "status": status
    }

    jobs.append(job)
    save_jobs()
    print("Job added successfully!\n")

def view_jobs():
    if not jobs:
        print("No jobs found.\n")
        return

    for i, job in enumerate(jobs, start=1):
        print(f"{i}. {job['company']} - {job['role']} - {job['status']}")
    print()

def update_job():
    view_jobs()
    if not jobs:
        return

    index = int(input("Enter job number to update: ")) - 1

    if 0 <= index < len(jobs):
        new_status = input("Enter new status: ")
        jobs[index]["status"] = new_status
        save_jobs()
        print("Job updated successfully!\n")
    else:
        print("Invalid job number\n")

def delete_job():
    view_jobs()
    if not jobs:
        return

    index = int(input("Enter job number to delete: ")) - 1

    if 0 <= index < len(jobs):
        deleted_job = jobs.pop(index)
        save_jobs()
        print(f"Deleted job at {deleted_job['company']} - {deleted_job['role']}\n")
    else:
        print("Invalid job number\n")

while True:
    print("1. Add Job")
    print("2. View Jobs")
    print("3. Update Job Status")
    print("4. Delete Job")
    print("5. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_job()
    elif choice == "2":
        view_jobs()
    elif choice == "3":
        update_job()
    elif choice == "4":
        delete_job()
    elif choice == "5":
        print("Good luck with your applications 💪")
        break
    else:
        print("Invalid choice\n")
