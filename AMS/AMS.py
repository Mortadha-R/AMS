import os
from json import loads
from PIL import Image
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
        print("Available Sections:")
        for index, section in enumerate(self.sections, start=1):
            print(f"{index}. Section {section}")
    
        try:
            section_index = int(input("Select section index to take attendance for: ")) - 1
            if section_index < 0 or section_index >= len(self.sections):
                raise IndexError("Selected section index is out of range.")
    
            selected_section = self.sections[section_index]
            section_filename = os.path.join("Sections", f"Section{selected_section}.txt")
    
            if not os.path.exists(section_filename):
                raise FileNotFoundError(f"Section file '{section_filename}' not found.")
    
            lecture_index = int(input("Select lecture index to take attendance for (from 1-20): ")) - 1
            if lecture_index < 0 or lecture_index >= 20:
                raise IndexError("Lecture index is out of range. Please enter a value from 1 to 20.")
    
            with open(section_filename, 'r') as section_file:
                lines = section_file.readlines()
    
            updated_lines = []
    
            for line in lines:
                st_id = line[4:line.find("|Name")]
                st_name = line[line.find("Name: ") + 6:line.find("|Lectures")]
                lectures_start = line.find("Lectures: [") + len("Lectures: [")
                lectures_end = line.find("]", lectures_start)
                lectures = line[lectures_start:lectures_end].split(",")
    
                status = input(f"Student name: {st_name} (A for absent, P for present): ").upper()
                if status not in ['A', 'P']:
                    print("Invalid input, marking as absent.")
                    status = 'A'
    
                # Update the specific lecture index
                lectures[lecture_index] = status
                updated_lectures = ",".join(lectures)
    
                # Reconstruct the line with updated lectures
                updated_line = f"ID: {st_id}|Name: {st_name}|Lectures: [{updated_lectures}]\n"
                updated_lines.append(updated_line)
    
            # Write the updated lines back to the file
            with open(section_filename, 'w') as section_file:
                section_file.writelines(updated_lines)
    
            print("Attendance recorded successfully.")
        except ValueError as e:
            print("Invalid input. Please enter valid numerical indices.")
        except IndexError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")



    def list_sections(self):
        print("your sections: ")
        print(self.sections)




def review_excuses(file_path):
    try:
        # Read the file
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Extract not reviewed excuses
        not_reviewed_excuses = [line.strip() for line in lines if "not reviewed" in line]

        if not not_reviewed_excuses:
            print("No excuses to review.")
            return

        # Display not reviewed excuses
        print("Not reviewed excuses:")
        for i, excuse in enumerate(not_reviewed_excuses):
            print(f"{i + 1}. {excuse}")

        # Prompt user for choice
        choice = int(input("Enter the index of the excuse you want to review: ")) - 1

        if choice < 0 or choice >= len(not_reviewed_excuses):
            raise IndexError("Selected excuse index is out of range.")

        selected_excuse = not_reviewed_excuses[choice]
        
        excuse_parts = selected_excuse.split('|')
        # Display excuse image
        img_path = excuse_parts[3].split("File:")[1].strip()
        Image.open(img_path).show()

        # Ask for acceptance or rejection
        decision = input(f"Is the excuse '{selected_excuse}' accepted or rejected? ").lower()
        if decision not in ['accepted', 'rejected']:
            raise ValueError("Invalid decision. Please enter 'accepted' or 'rejected'.")

        # Parse the excuse details
        sender_id = excuse_parts[0].split(': ')[1].strip()
        section = excuse_parts[1].split(': ')[1].strip()
        lecture_index = int(excuse_parts[2].split(': ')[1].strip()) - 1

        # Update the section file if accepted
        if decision == "accepted":
            section_filename = os.path.join("Sections", f"Section{section}.txt")

            if not os.path.exists(section_filename):
                raise FileNotFoundError(f"Section file '{section_filename}' not found.")

            with open(section_filename, 'r') as section_file:
                section_lines = section_file.readlines()

            updated_section_lines = []
            student_found = False

            for line in section_lines:
                if f"ID: {sender_id}|" in line:
                    student_found = True
                    # Extract lectures and update the specified lecture index
                    lectures_start = line.find("Lectures: [") + len("Lectures: [")
                    lectures_end = line.find("]", lectures_start)
                    lectures = line[lectures_start:lectures_end].split(",")

                    if lectures[lecture_index] == 'A':
                        lectures[lecture_index] = 'P'  # Mark the lecture as present

                    updated_lectures = ",".join(lectures)
                    updated_line = f"ID: {sender_id}|Name: {line.split('|')[1].split(': ')[1]}|Lectures: [{updated_lectures}]\n"
                    updated_section_lines.append(updated_line)
                else:
                    updated_section_lines.append(line)

            if not student_found:
                raise ValueError(f"Student ID '{sender_id}' not found in section '{section}'.")

            # Write the updated lines back to the section file
            with open(section_filename, 'w') as section_file:
                section_file.writelines(updated_section_lines)

        # Update the excuses file
        with open(file_path, 'w') as f:
            for line in lines:
                if selected_excuse in line:
                    f.write(line.replace("not reviewed", decision))
                else:
                    f.write(line)

        print(f"Excuse '{selected_excuse}' has been {decision}.")
    except FileNotFoundError as e:
        print(e)
    except IndexError as e:
        print(e)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

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
            sections = user.list_sections()
            cont = input("press any key to continue: ")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif facultyChose == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            user.record_attendance()
            cont = input("press any key to continue: ")
            os.system('cls' if os.name == 'nt' else 'clear')
        elif facultyChose == '3':
            logout()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Invalid choice. Please enter a number between 1 and 3.")

select()
