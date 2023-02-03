# Homework 1
# CS 4395 NLP
# Zubair Shaik

import pathlib
import pickle
import sys
import re


# Created a person object to contain all the employee attributes listed in the csv file
class Person:
    def __init__(self, last, first, middle, empID, phone):
        self.last = last
        self.first = first
        self.middle = middle
        self.empID = empID
        self.phone = phone

    def display(self):
        print(f'Employee ID: {self.empID}')
        print(f'\t{self.first} {self.middle} {self.last}')
        print(f'\t{self.phone}\n')


# This function handles all the employee text processing line by line
def process_lines(employeeList):
    # Dictionary to hold all the correctly formatted employees
    employee_handbook = {}
    for emp in employeeList:
        # split the line by comma then access each specific index of the list and store it in a variable
        attributes = emp.split(',')

        last = attributes[0].capitalize()
        first = attributes[1].capitalize()

        middle = attributes[2]
        # If there's no middle initial put X as default
        if middle == '':
            middle = 'X'
        else:
            middle = middle[0:1].capitalize()

        # Regex check to see if ID is valid otherwise keep asking for new ID
        empID = re.match(r'[a-zA-Z]{2}\d{4}', attributes[3])
        while not empID:
            print(f'ID invalid: {attributes[3]}')
            print('ID is two letters followed by 4 digits')
            userInput = input("Please enter a valid id: ")
            empID = re.match(r'[a-zA-Z]{2}\d{4}', userInput)
        empID = empID.group()

        # Regex check to see if phone is valid otherwise keep asking for new phone
        phone = re.match(r'[a-zA-Z]{2}\d{4}', attributes[4])
        while not phone:
            print(f'Phone {attributes[4]} is invalid')
            print('Enter Phone Number in form 123-456-7890')
            userInput = input("Enter Phone Number: ")
            phone = re.match(r'^[0-9]{3}-[0-9]{3}-[0-9]{4}$', userInput)
        phone = phone.group()

        # Create new person object with all the passed in variables
        person = Person(last, first, middle, empID, phone)

        # Check if ID is already present in dictionary, otherwise add it to dictionary
        if empID in employee_handbook:
            print('ID already exists')
        else:
            employee_handbook[empID] = person
    return employee_handbook


# This is the main driver function that starts the program and reads and writes to the pickle file
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    rel_path = sys.argv[1]
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in = f.read().splitlines()

    employees = process_lines(text_in[1:])

    pickle.dump(employees, open('employees.pickle', 'wb'))

    employees_in = pickle.load(open('employees.pickle', 'rb'))

    print('\n\nEmployee List:')

    for emp_id in employees_in.keys():
        employees_in[emp_id].display()
