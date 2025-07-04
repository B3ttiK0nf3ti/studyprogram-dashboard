from classes import study_program, Semester, Module, DataManager, ProgressMonitor
from dataManager import DataManager
from progressMonitor import ProgressMonitor
from datetime import date
from typing import List, Dict, Any

STUDY_DATA_FILE = "study_data.json"

class CLIController:
    """
    Class representing a command-line interface controller.
    """
    def __init__(self):
        self.data_manager = DataManager(STUDY_DATA_FILE)
        self.study_program = study_program("Informatik", 6)
        self.progress_monitor = ProgressMonitor(self.study_program)

    def display_menu(self):
        print("\n--- Study Progress Dashboard ---")
        print("1. Add Module")
        print("2. Add Grades")
        print("3. Display Progress")
        print("4. Display Dashboard")
        print("5. Exit")
    
    def handle_user_input(self):
        while True:
            self.display_menu()
            choice = input("Please choose an Option: ")
            if choice == "1":
                self.add_module()
            elif choice == "2":
                self.enter_grades()
            elif choice == "3":
                self.show_progress()
            elif choice == "4":
                self.show_dashboard()
            elif choice == "5":
                print("Program ended.")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def add_module(self):
        title = input("Enter module name: ")
        ects = int(input("Enter ECTS points: "))
        semester_number = int(input("Enter semester number: "))
        
        # Find or create the semester
        semester = next((s for s in self.study_program.semesters if s.number == semester_number), None)
        if not semester:
            semester = Semester(semester_number)
            self.study_program.semesters.append(semester)
        
        # Create and add the module
        module = Module(title, ects)
        semester.add_module(module)
        print(f"Module '{title}' added to semester {semester_number}.")
    
    def input_grades(self):
        semester_number = int(input("Enter semester number: "))
        semester = next((s for s in self.study_program.semesters if s.number == semester_number), None)
        
        if not semester:
            print(f"No semester found with number {semester_number}.")
            return
        
        module_name = input("Enter module name: ")
        module = next((m for m in semester.get_modules() if m.name == module_name), None)
        
        if not module:
            print(f"No module found with name '{module_name}' in semester {semester_number}.")
            return
        
        grade = float(input("Enter grade: "))
        module.add_grade(grade)
        print(f"Grade {grade} added to module '{module_name}'.")
    
    def calc_progress(self):
        progress = self.progress_monitor.calc_study_progress()
        print(f"Study progress: {progress:.2f}%")
    
    def show_dashboard(self):
        print("\n--- Dashboard ---")
        print(f"Average Grade: {self.progress_monitor.calc_grade_average():.2f}")
        print(f"Pass Quote: {self.progress_monitor.calc_pass_quote():.2f}%")
        print(f"Study Progress: {self.progress_monitor.calc_study_progress():.2f}%")
        print(f"Average Learning Time: {self.progress_monitor.calc_average_learning_time():.2f} hours")

    def show_progress(self):
        print("\n--- Study Progress ---")
        for semester in self.study_program.semesters:
            print(f"Semester {semester.number}:")
            for module in semester.get_modules():
                print(f"  Module: {module.name}, ECTS: {module.ects}, Status: {module.status}")
                if module.exam_performance:
                    print(f"    Exam Performance: {module.exam_performance.grade} (Passed: {module.exam_performance.passed})")
                if module.learning_times:
                    print("    Learning Times:")
                    for lt in module.learning_times:
                        print(f"      Date: {lt.date}, Hours: {lt.hours}")  
                else:
                    print("    No learning times recorded.")   
    
if __name__ == "__main__":
    cli_controller = CLIController()
    cli_controller.handle_user_input()
    data_manager = DataManager(STUDY_DATA_FILE)
    data_manager.save_data(cli_controller.study_program.serialize_object(), STUDY_DATA_FILE)
    print(f"Study program data saved to '{STUDY_DATA_FILE}'.")
    data_manager.save_data(cli_controller.study_program.serialize_object(), "study_data.json")
    print("Study program data saved to 'study_data.json'.")