import os
from json import loads
import tkinter as tk
from tkinter import filedialog

# Admin login info
admin_name = "admin"
admin_password = "admin"


class Student:
    def __init__(self, st_id, name, sections):
        self.st_id = st_id
        self.name = name
        self.sections = sections


    def read_attendance(self):
        absent_lectures_by_section = {}

        # Iterate over each section assigned to the student
        for section in self.sections:
            section_filename = os.path.join("Sections", f"Section{section}.txt")
            absent_lectures = []

            # Read attendance data from the section's file
            with open(section_filename, 'r') as attendance_file:
                for line in attendance_file:
                    if f"ID: {self.st_id}|Name: {self.name}|" in line:
                        # Extract the part containing lectures and remove unwanted characters
                        lectures_part = line.split("Lectures: ")[1].strip()
                        lectures_cleaned = lectures_part.strip('[]').split(",")

                        # Find indices of 'A' (absent) in the attendance list
                        for index, status in enumerate(lectures_cleaned):
                            if status == "A":
                                # Get the corresponding lecture number (index + 1)
                                lecture_number = index + 1
                                absent_lectures.append(lecture_number)

            # Store absent lectures for the current section
            absent_lectures_by_section[section] = absent_lectures

        # Print absent lectures for each section
        for section, absent_lectures in absent_lectures_by_section.items():
            if absent_lectures:
                print(f"Section {section}: Absent in the following lectures:")
                for lecture_number in absent_lectures:
                    print(f"Lecture {lecture_number}")
            else:
                print(f"Section {section}: No absences recorded.")

        return absent_lectures_by_section        


    # this function replaced with read_attendance
    #def list_attendance(self):





    def upload_excuse(self):
        attendance_data = self.read_attendance()
        section_index = 0
        lecture_index = 0

        print("Available Sections:")
        for section in attendance_data:
            section_index += 1
            print(f"{section_index}- Section {section}")

        section_choice = input("Choose section index: ")

        try:
            section_choice = int(section_choice)
            if 1 <= section_choice <= len(attendance_data):
                selected_section = list(attendance_data.keys())[section_choice - 1]
                absent_lectures = attendance_data[selected_section]

                if absent_lectures:
                    print(f"Section {selected_section}: Absent in the following lectures:")
                    for lecture_number in absent_lectures:
                        lecture_index += 1
                        print(f"Lecture: {lecture_number}")


                    lecture_choice = input("Choose lecture index: ")

                    root = tk.Tk()
                    root.deiconify()

                    file_path = filedialog.askopenfilename(
                        title="Select Excuse File",
                        filetypes=[
                            ("Image Files", "*.jpg; *.jpeg; *.png; *.gif"),
                            ("PDF Files", "*.pdf"),
                            ("Text Files", "*.txt")
                        ]
                    )

                    if file_path:
                        print("Selected File:", file_path)

                        output_file_path = 'Excuses_info.txt'
                        we = f"Sender ID: {self.st_id} | Section: {selected_section} | Lecture Index: {lecture_choice} |  File: {file_path} | not reviewed"

                        # Write the content to the output file in append mode
                        with open(output_file_path, 'a') as output_file:
                            output_file.write(we + '\n')  # Append the excuse followed by a newline

                        print("The file was sent successfully")
                    else:
                        print("No file selected.")

                    root.destroy()  # Destroy the tkinter window after file selection

                else:
                    print(f"Section {selected_section}: No absences recorded.")
            else:
                print("Invalid section index. Please choose a valid section index.")

        except ValueError:
            print("Invalid input. Please enter a valid section index.")

        except IndexError:
            print("Invalid section index. Please choose a valid section index.")


class FacultyMember:
    def __init__(self, fac_id, name, sections):
        self. fac_id = fac_id
        self.name = name
        self.sections = sections

    def record_attendance(self):
        pass

    def list_sections(self):
        pass



def review_excuses(file_path):
    try:
        # Read the file
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Extract not reviewed excuses
        not_reviewed_excuses = []
        for line in lines:
            if "not reviewed" in line:
                not_reviewed_excuses.append(line.strip())
                
        #Check that there are unreviewed excuses.
        if not not_reviewed_excuses:
            print("There are no unreviewed excuses.")
            return
            
        # Display not reviewed excuses
        print("Not reviewed excuses:")
        for i, excuse in enumerate(not_reviewed_excuses):
            print(f"{i + 1}. {excuse}")

        # Prompt user for choice
        choice = int(input("Enter the index of the excuse you want to review: ")) - 1
        try:
            selected_excuse = not_reviewed_excuses[choice]
    
            # Ask for acceptance or rejection
            decision = input(f"Is the excuse '{selected_excuse}' accepted or rejected? ").lower()
    
            # Update the file
            with open(file_path, 'w') as f:
                for line in lines:
                    if selected_excuse in line:
                        if decision == "accepted":
                            f.write(line.replace("not reviewed", "accepted"))
                        elif decision == "rejected":
                            f.write(line.replace("not reviewed", "rejected"))
                        else:
                            f.write(line)
                    else:
                        f.write(line)
            if decision == "accepted" or decision == "rejected":
                print(f"Excuse '{selected_excuse}' has been {decision}.")
            else:
                print("Invalid Choice the excuse has not been modified.")
        except IndexError:
            print("The selected excuse is not in the list.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")




def login(user_type = 3):
    os.system('cls')

    print("Enter your username and password.")
    username = input("Username: ")
    password = input("Password: ")

    if user_type == 1:
        if username == admin_name and password == admin_password:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Welcome, {username.capitalize()}!")
        else:
            response = input("Invalid user name or password! try again?(Y/N)").capitalize()
            if response == "Y" or response == "Yes":
                login(1)
            else:
                exit_program()
    elif user_type == 2:
        with open("Faculty_member_info.txt", 'r') as faculty_info:

            for line in faculty_info:
                # Search the file for the input ID and password
                current_fac_id = line[4:line.find("|Password")]
                current_password = line[(line.find("|Password: ") + 11): line.find("|Name")]
                # Compare input with ID's and names in file

                if username == current_fac_id and password == current_password:

                    # Gather user info from file and turn into a faculty member object
                    name = line[line.find("Name: ") + 6:line.find("|Sections")]
                    # Turn sections string into a python list
                    sections = loads(line[line.find("Sections: ") + 10:])

                    return FacultyMember(current_fac_id, name, sections)
            else:
                response = input("Invalid user name or password! try again?(Y/N)").capitalize()
                if response == "Y" or response == "Yes":
                    return login(2)
                else:
                    exit_program()

    # Student login process
    elif user_type == 3:
        with open('Students_info.txt', 'r') as student_info:

            for line in student_info:
               # Search the file for the input ID and password
               current_st_id = line[4:line.find("|Password")]
               current_password = line[(line.find("|Password: ") + 11): line.find("|Name")]
               # Compare input with ID's and names in file

               if username == current_st_id and password == current_password:

                   # Gather user info from file and turn into a Student object
                   name = line[line.find("Name: ") + 6:line.find("|Sections")]
                   # Turn sections string into a python list
                   sections = loads(line[line.find("Sections: ") + 10:])

                   return Student(current_st_id, name, sections)
            else:
               response = input("Invalid user name or password! try again?(Y/N)").capitalize()
               if response == "Y" or response == "Yes":
                   return login(3)
               else:
                   exit_program()

def logout():
    os.system('cls' if os.name == 'nt' else 'clear')
    current_user = None
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Logged out successfully.")
    cont = input("press any key to continue: ")
    select()


def exit_program():
  print("Exiting program...")
  os.system('cls' if os.name == 'nt' else 'clear')
  exit()
  

def select():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to The Attendance Monitoring System")
    print("Are you:")
    print("1. Administrator")
    print("2. Faculty member")
    print("3. Student")
    print("4. Exit")

    userType = input("Enter your choice (1-4): ")
    if userType == '1':
        login(1)
        adminMenu()
    elif userType == '2':
        user = login(2)
        facultyMenu(user)
    elif userType == '3':
        user = login(3)
        studentMenu(user)
    elif userType == '4':
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Invalid choice. Please enter a number between 1 and 4.")
        input("Press any key to continue: ")
        select()


def studentMenu(user):
    print(f"Hello {user.name.capitalize()}!\n")

    while True:
        print("1. List Sections")
        print("2. Upload Excuse")
        print("3. Logout")

        studentChose = input("Enter your choice (1-3): ")

        if studentChose == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            absent_lectures = user.read_attendance()
            # if absent_lectures:
            #     print("Absent in the following lectures:")
            #     for lecture_number in absent_lectures:
            #         print(f"Lecture {lecture_number}")
            # else:
            #     print("No absences recorded.")

            cont = input("press any key to continue: ")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif studentChose == '2':
            os.system('cls' if os.name == 'nt' else 'clear')

            user.upload_excuse()
            cont = input("press any key to continue: ")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif studentChose == '3':
            logout()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid choice. Please enter a number between 1 and 3.")


def adminMenu():

    while True:
        print("1. Review Excuses")
        print("2. Logout")

        adminChose = input("Enter your choice (1-2): ")

        if adminChose == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            filename = "Excuses_info.txt"
            review_excuses(filename)
            cont = input("press any key to continue: ")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif adminChose == '2':
            logout()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid choice. Please enter a number between 1 and 2.")


def facultyMenu(user):
    print(f"Hello {user.name.capitalize()}!")

    while True:
        print("Faculty Menu")
        print("1. List Sections")
        print("2. Record Attendance")
        print("3. Logout")

        facultyChose = input("Enter your choice (1-3): ")

        if facultyChose == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Sections:")
            print("1- FOS/6")
            print("1- Electric Circuits/1")
            cont = input("press any key to continue: ")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif facultyChose == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Students List:")
            print("1- Mohammed")
            print("2- Ahmed")
            print("3- Ali")
            cont = input("press any key to continue: ")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif facultyChose == '3':
            logout()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid choice. Please enter a number between 1 and 3.")

select()
