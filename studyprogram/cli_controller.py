from classes import StudyProgram, Semester, Module, ModuleStatus
from classes import ExamPerformance, LearningTime
from data_manager import DataManager
from progress_monitor import ProgressMonitor
from datetime import date
import plotext as plt
import re

STUDY_DATA_FILE = "study_data.json"
class CLIController:
    def __init__(self, data_manager: DataManager, study_program: StudyProgram, progress_monitor: ProgressMonitor):
        self.data_manager = data_manager
        self.study_program = study_program
        self.progress_monitor = progress_monitor

    def get_semester(self, number: int):
        return next((s for s in self.study_program.semesters if s.number == number), None)

    def get_module(self, semester, module_name: str):
        normalized_input = self.normalize_string(module_name)
        return next((m for m in semester.get_modules() if self.normalize_string(m.title) == normalized_input), None)

    def list_modules_in_semester(self, semester):
        if not semester.modules:
            print("  No modules found.")
            return
        print("  Available modules:")
        for module in semester.modules:
            print(f"   - {module.title} ({module.ects} ECTS, Status: {module.status})")

    def display_menu(self):
        print("\n--- STUDY PROGRESS DASHBOARD ---")
        print("1. Add Module")
        print("2. Add Grades")
        print("3. Display Progress")
        print("4. Display Dashboard")
        print("5. Add Learning Time") 
        print("6. Edit Module")
        print("7. Exit")
    
    def handle_user_input(self):
        while True:
            self.display_menu()
            choice = input("Please choose an Option: ")
            if choice == "1":
                self.add_module()
            elif choice == "2":
                self.input_grades()
            elif choice == "3":
                self.show_progress()
            elif choice == "4":
                self.show_dashboard()
            elif choice == "5":
                self.add_learning_time() 
            elif choice == "6":
                self.edit_module()
            elif choice == "7":
                print("Program ended.")
                break
            else:
                print("Invalid choice. Please try again.")

    def normalize_string(self, input_string: str) -> str:
        return re.sub(r'\s+', ' ', input_string.strip().lower())
    
    def add_module(self):
        title = input("Enter module name: ")
        normalized_title = self.normalize_string(title)

        # ECTS points input with validation
        while True:
            try:
                ects = int(input("Enter ECTS points (only 5 or 10 allowed): "))
                if ects in (5, 10):
                    break
                else:
                    print("Invalid input. ECTS points must be either 5 or 10.")
            except ValueError:
                print("Invalid input. Please enter a valid integer (5 or 10).")
    

        # Semester number input with validation
        while True:
            try:
                semester_number = int(input("Enter semester number (1 to 6): "))
                if 1 <= semester_number <= 6:
                    break
                else:
                    print("Invalid input. Semester number must be between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a valid integer for the semester number.")
        
        # Find or create the semester
        semester = next((s for s in self.study_program.semesters if s.number == semester_number), None)
        if not semester:
            semester = Semester(semester_number)
            self.study_program.semesters.append(semester)

        # Check for duplicate module
        existing_module = next(
            (m for m in semester.modules if m.normalized_title == normalized_title),
            None
        )

        if existing_module:
            print(f"Module '{title}' already exists in semester {semester_number}.")
            return
        
        # Create and add the module
        module = Module(normalized_title, ects, status=ModuleStatus.OPEN)
        semester.add_module(module)

        print(f"Module '{title}' added to semester {semester_number}.")

        self.data_manager.save_data(self.study_program.to_dict())

    def edit_module(self):
        # Semester number input with validation
        while True:
            try:
                semester_number = int(input("Enter semester number (1-6): "))
                if 1 <= semester_number <= 6:
                    break
                else:
                    print("Invalid input. Semester number must be between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a valid integer for the semester number.")

        semester = self.get_semester(semester_number)
        if not semester:
            print(f"No semester found with number {semester_number}.")
            return
        
        self.list_modules_in_semester(semester)

        module_name = input("Enter module name: ")
        module = self.get_module(semester, module_name)

        print(f"\nEditing module '{module.title}' in semester {semester_number}:")
        print("1. Edit Module Name")
        print("2. Edit ECTS Points")
        print("3. Move to Another Semester")
        print("4. Delete Module")       
        print("5. Cancel")

        choice = input("Select an option: ")

        if choice == "1":
            new_title = input("Enter new module name: ")
            normalized_new_title = self.normalize_string(new_title)

            # Check for duplicate module name
            if any(self.normalize_string(m.title) == normalized_new_title and m != module for m in semester.get_modules()):
                print(f"Module '{new_title}' already exists in semester {semester_number}.")
                return
            
            module.title = normalized_new_title
            print(f"Module name changed to '{new_title}'.")
        elif choice == "2":
            while True:
                try:
                    new_ects = int(input("Enter new ECTS points (only 5 or 10 allowed): "))
                    if new_ects in (5, 10):
                        module.ects = new_ects
                        print(f"ECTS points changed to {new_ects}.")
                        break
                    else:
                        print("Invalid input. ECTS points must be either 5 or 10.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer (5 or 10).")
        elif choice == "3":
            while True:
                try:
                    new_semester_number = int(input("Enter new semester number (1-6): "))
                    if 1 <= new_semester_number <= 6:
                        break
                    else:
                        print("Invalid input. Semester number must be between 1 and 6.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer for the semester number.")

            new_semester = next((s for s in self.study_program.semesters if s.number == new_semester_number), None)
            if not new_semester:
                new_semester = Semester(new_semester_number)
                self.study_program.semesters.append(new_semester)

            # Remove module from current semester and add to new semester
            semester.modules.remove(module)
            new_semester.add_module(module)
            print(f"Module '{module.title}' moved to semester {new_semester_number}.")

        elif choice == "4":
            confirm = input(f"Are you sure you want to delete the module '{module.title}'? (y/n): ")
            if confirm.lower() == 'y':
                semester.modules.remove(module)
                print(f"Module '{module.title}' deleted from semester {semester_number}.")
            else:
                print("Deletion cancelled.")
        elif choice == "5":
            print("Cancelled editing.")
            return
        else:
            print("Invalid option.")

        self.data_manager.save_data(self.study_program.to_dict())
        print("Changes saved successfully.")

    
    def input_grades(self):

        # Semester number input with validation
        while True:
                try:
                    semester_number = int(input("Enter semester number (1-6): "))
                    if 1 <= semester_number <= 6:
                        break
                    else:
                        print("Invalid input. Semester number must be between 1 and 6.")
                except ValueError:
                    print("Invalid input. Please enter a valid integer for the semester number.")

        semester = self.get_semester(semester_number)
        if not semester:
            print(f"No semester found with number {semester_number}.")
            return

        self.list_modules_in_semester(semester)

        module_name = input("Enter module name: ")
        module = self.get_module(semester, module_name)

        if not module:
            print(f"No module found with name '{module_name}' in semester {semester_number}.")
            return
        
        # Check if module is already passed
        if module.status == ModuleStatus.PASSED:
            print(f"Module '{module_name}' has already been passed. No more grades can be entered.")
            return

        # Check if attempts >= 3
        if len(module.exam_performances) >= 3:
            print(f"Module '{module_name}' has already been attempted 3 times and is considered failed.")
            module.status = ModuleStatus.FAILED
            return

        # Grade input with validation (allowing decimal points)
        while True:
            try:
                grade = float(input("Enter grade (1.0 to 5.0, where ≤4.0 is passing): ")
).replace(',', '.')
                if 1.00 <= grade <= 5.00:
                    break
                else:
                    print("Invalid input. Grade must be between 1.00 and 5.00.")
            except ValueError:
                print("Invalid input. Please enter a valid number for the grade.")

        attempt = len(module.exam_performances) + 1
        passed = grade <= 4.0

        # Add exam performance correctly
        module.exam_performances.append(ExamPerformance(grade=grade, attempt=attempt, passed=passed))

        # Update status
        module.status = ModuleStatus.PASSED if passed else ModuleStatus.FAILED

        print(f"Grade {grade} added to module '{module_name}'.")

        self.data_manager.save_data(self.study_program.to_dict())
    
    def add_learning_time(self):

        # Semester number input with validation
        while True:
            try:
                semester_number = int(input("Enter semester number (1-6): "))
                if 1 <= semester_number <= 6:
                    break
                else:
                    print("Invalid input. Semester number must be between 1 and 6.")
            except ValueError:
                print("Invalid input. Please enter a valid integer for the semester number.")
                return

        semester = self.get_semester(semester_number)
        if not semester:
            print(f"No semester found with number {semester_number}.")
            return
        
        self.list_modules_in_semester(semester)

        module_name = input("Enter module name: ")
        module = self.get_module(semester, module_name)


        if not module:
            print(f"No module found with name '{module_name}' in semester {semester_number}.")
            return

        while True:
            try:
                hours = float(input("Enter learning hours: ").replace(",", "."))
                if hours >= 0:
                    break
                else:
                    print("Invalid input. Learning hours must be a non-negative number.")
            except ValueError:
                print("Invalid input. Please enter a valid number for the learning hours.")
                return

        today = date.today()
        module.learning_times.append(LearningTime(date=today, hours=hours))

        print(f"Added {hours} learning hours to module '{module_name}' on {today}.")

        self.data_manager.save_data(self.study_program.to_dict())
    
    def calc_progress(self):
        progress = self.progress_monitor.calc_study_progress()
        print(f"Study progress: {progress:.2f}%")
    
    def show_dashboard(self):
        print("\n--- DASHBOARD ---")
        print(f"Timeline: Sem 1 - {self.study_program.regular_study_period} (3 Years)")
        
        # Total number of semesters and calculated progress
        completed_percentage = self.progress_monitor.calc_study_progress()
        
        # Display study progress
        print("=" * 30)
        print(f"Study Progress: {completed_percentage:.1f}%")
        
        # Progress bar over the entire timeline (6 semesters)
        progress_bar_length = 40  # Length of the progress bar
        completed_length = int(progress_bar_length * completed_percentage / 100)
        progress_bar = '█' * completed_length + '-' * (progress_bar_length - completed_length)
        print(f"Timeline: |{progress_bar}| {completed_percentage:.1f}% completed")

        avg_grade = self.progress_monitor.calc_grade_average()
        study_progress = self.progress_monitor.calc_study_progress()
        avg_learning_time = self.progress_monitor.calc_average_learning_time()

        print(f"\nAvg. Grade: {avg_grade:.2f} | Study Prog.: {study_progress:.1f}% | Avg. Learn Time: {avg_learning_time:.1f} h")
        
        # Calculation of planned learning time and actual learning time
        planned_learning_time = sum(module.ects * 25 for semester in self.study_program.semesters for module in semester.modules)
        actual_learning_time = sum(
            sum(lt.hours for lt in module.learning_times)
            for semester in self.study_program.semesters for module in semester.modules
        )

        print("\nLearning Time (Module):")
        print(f"  Planned Learning Time: {planned_learning_time:.1f} hours")
        print(f"  Actual Learning Time: {actual_learning_time:.1f} hours")
        if actual_learning_time < planned_learning_time:
            print(f"  You are behind by {planned_learning_time - actual_learning_time:.1f} hours.")
        elif actual_learning_time > planned_learning_time:
            print(f"  You are ahead by {actual_learning_time - planned_learning_time:.1f} hours.")
        else:
            print("  You are right on track with your planned learning time.")

        print("\nGrade Progression:")
        self.plot_terminal_grade_progression()

        print("\nLearning Time (Module):")
        self.plot_terminal_learning_time()

        print("\nExam Status:")
        self.show_terminal_exam_status()

    def show_progress(self):
        print("\n--- STUDY PROGRESS ---")
        for semester in self.study_program.semesters:
            print(f"Semester {semester.number}:")
            for module in semester.get_modules():
                print(f"  Module: {module.title}, ECTS: {module.ects}, Status: {module.status}")
                if module.exam_performances:
                    for ep in module.exam_performances:
                        print(f"    Exam Performance: Grade: {ep.grade}, Attempt: {ep.attempt}, Passed: {ep.passed}")
                else:
                    print("    No exam performances recorded.")
                if module.learning_times:
                    print("    Learning Times:")
                    for lt in module.learning_times:
                        print(f"      Date: {lt.date}, Hours: {lt.hours}")
                else:
                    print("    No learning times recorded.")
    
    def display_progress_bar(self, label: str, value: float, max_value: float = 100, bar_length: int = 40):
        # Display a progress bar in the terminal
        if bar_length is None:
            bar_length = max(20, 40)  # Default to 40 if None is provided
        
        # Ensure value is within the range [0, max_value]
        value = max(0, min(value, max_value))
        
        # Calculate the filled length of the bar
        filled_length = int(bar_length * value / max_value)
        
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        # Format the output
        percentage = (value / max_value) * 100
        print(f"{label:6}: |{bar}| {percentage:5.1f}%")

    def plot_terminal_grade_progression(self):
        import plotext as plt
        import math

        semester_grades = {}

        # Iterate through semesters and modules to collect grades
        for semester in self.study_program.semesters:
            for module in semester.modules:
                for ep in module.exam_performances:
                    if ep.passed and ep.grade is not None:
                        semester_grades.setdefault(semester.number, []).append(ep.grade)

        if not semester_grades:
            print("No exam performances available for plotting.")
            return

        semesters = list(range(1, 7))
        avg_grades = []

        for s in semesters:
            grades = semester_grades.get(s)
            if grades:
                avg = sum(grades) / len(grades)
                avg_grades.append(avg)
            else:
                avg_grades.append(float('nan'))

        # Invert grades for plotting (1.0 becomes 5.0, 5.0 becomes 1.0)
        inverted_grades = [6 - g if not math.isnan(g) else float('nan') for g in avg_grades]

        # Define dummy values for the plot to ensure the y-axis shows all grades
        dummy_x = [0, 0]
        dummy_y = [6 - 1.0, 6 - 5.0]  # 1.0 und 5.0 invertiert = 5.0 und 1.0

        # Define the grade ticks for the y-axis
        grade_ticks = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        inverted_ticks = [6 - g for g in grade_ticks]

        # Plot
        plt.clear_figure()
        plt.plotsize(100, 25)
        plt.title("Average Grade Progression")
        plt.xlabel("Semester")
        plt.ylabel("Grade")
        plt.xlim(1, 6)
        plt.xticks(semesters)
        plt.yticks(inverted_ticks, [f"{g:.2f}" for g in grade_ticks])

        # Dummy data to ensure the y-axis shows all grades
        plt.scatter(dummy_x, dummy_y, color=None)  

        plt.plot(semesters, inverted_grades, marker='hd', color="cyan", label="Ø Grade")
        plt.grid(False)
        plt.show()

    def show_terminal_exam_status(self):
        passed = 0
        open = 0
        failed = 0

        for semester in self.study_program.semesters:
            for module in semester.modules:
                if module.status == ModuleStatus.PASSED:
                    passed += 1
                elif module.status == ModuleStatus.FAILED:
                    failed += 1
                else:
                    open += 1

        total = passed + open + failed

        if total == 0:
            print("Keine Module zum Anzeigen des Prüfungsstatus verfügbar.")
            return

        print("\n--- EXAM STATUS OVERVIEW ---")
        self.display_progress_bar("Passed", (passed / total) * 100)
        self.display_progress_bar("Open", (open / total) * 100)
        self.display_progress_bar("Failed", (failed / total) * 100)

    def plot_terminal_learning_time(self):
        module_titles = []
        actual_times = []
        planned_times = []

        for semester in self.study_program.semesters:
            for module in semester.modules:
                module_titles.append(module.title)
                actual_time = sum(lt.hours for lt in module.learning_times)
                actual_times.append(actual_time)
                planned_times.append(module.ects * 25)

        if module_titles:
            x = list(range(len(module_titles)))  # x-Achse numerisch

            plt.clear_figure()
            plt.plotsize(150, 20)
            plt.title("Learning Time per Module")
            plt.xlabel("Modules")
            plt.ylabel("Hours")

            # Plot actual and planned learning times side by side
            plt.bar(x, actual_times, label="Actual", color="cyan", width=0.2)
            plt.bar([i + 0.2 for i in x], planned_times, label="Planned", color="red", width=0.2)
            plt.xticks([i + 0.2 for i in x], module_titles)

            plt.show()
        else:
            print("Keine Module mit Lernzeiten zum Plotten vorhanden.")

if __name__ == "__main__":
    cli_controller = CLIController()
    cli_controller.handle_user_input()