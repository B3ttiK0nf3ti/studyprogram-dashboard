from enum import Enum
from datetime import date
import re
from typing import List

class ModuleStatus(Enum):
    """
    Enum representing the status of a module.
    """
    OPEN = "open"
    PASSED = "passed"
    FAILED = "failed"

class ExamPerformance:
    """
    Class representing the performance of a student in an exam.
    """
    def __init__(self, grade: float, attempt: int, passed: bool):
        self.grade = grade
        self.attempt = attempt
        self.passed = passed

    def __repr__(self):
        return f"ExamPerformance(grade={self.grade}, attempt={self.attempt}, passed={self.passed})"
    
    def is_passed(self) -> bool:
        """
        Check if the exam was passed.
        """
        return self.passed
    
class LearningTime:
    """
    Class representing the learning time for a student.
    """
    def __init__(self, date: date, hours: float):
        self.date = date
        self.hours = hours

    def __repr__(self):
        return f"LearningTime(date={self.date} hours={self.hours})"
    
    def get_learning_time(self) -> float:
        """
        Get the number of hours spent learning.
        """
        return self.hours

class Module:
    """
    Class representing a module in a course.
    """
    def __init__(self, title: str, ects: int, status: ModuleStatus):
        self.title = title
        self.normalized_title = re.sub(r'\s+', ' ', title.strip().lower())
        self.ects = ects
        self.status = status
        self.exam_performances: List[ExamPerformance] = []
        self.learning_times: List[LearningTime] = []

    def get_grade(self) -> float:
        """
        Get the average grade for the module.
        """
        if not self.exam_performances:
            return 0.0
        total_grade = sum(performance.grade for performance in self.exam_performances)
        return total_grade / len(self.exam_performances)
    
    def to_dict(self) -> dict:
        """
        Convert the module to a dictionary representation.
        """
        return {
            "title": self.title,
            "ects": self.ects,
            "status": self.status.value,
            "exam_performances": [
                {"grade": e.grade, "attempt": e.attempt, "passed": e.passed}
                for e in self.exam_performances
            ],
            "learning_times": [
                {"date": lt.date.isoformat(), "hours": lt.hours}
                for lt in self.learning_times
            ]
        }
    
    @staticmethod
    def from_dict(data: dict):
        """
        Create a Module instance from a dictionary representation.
        """
        module = Module(
            title=data["title"],
            ects=data["ects"],
            status=ModuleStatus(data["status"])
        )
        for exam in data.get("exam_performances", []):
            module.exam_performances.append(ExamPerformance(
                grade=exam["grade"],
                attempt=exam["attempt"],
                passed=exam["passed"]
            ))
        for learning_time in data.get("learning_times", []):
            module.learning_times.append(LearningTime(
                date=date.fromisoformat(learning_time["date"]),
                hours=learning_time["hours"]
            ))
        return module
    
    def add_exam_performance(self, performance: ExamPerformance):
        """
        Add an exam performance to the module.
        """
        self.exam_performances.append(performance)

    def add_learning_time(self, learning_time: LearningTime):
        """
        Add a learning time entry for the module.
        """
        self.learning_times.append(learning_time)

    def __repr__(self):
        return f"Module(name={self.title}, status={self.status}, exam_performances={self.exam_performances}, learning_times={self.learning_times}, ects={self.ects})"

class Semester:
    """
    Class representing a semester in a course.
    """
    def __init__(self, number: int):
        self.number = number
        self.modules: List[Module] = []

    def add_module(self, module: Module):
        """
        Add a module to the semester.
        """
        self.modules.append(module)

    def get_modules(self) -> List[Module]:
        """
        Get the list of modules in the semester.
        """
        return self.modules
    
    def to_dict(self) -> dict:
        return {
            "number": self.number,
            "modules": [module.to_dict() for module in self.modules]
        }
    
    @staticmethod
    def from_dict(data: dict):  
        """
        Create a Semester instance from a dictionary representation.
        """
        semester = Semester(
            number=data["number"]
        )
        for module_data in data.get("modules", []):
            semester.add_module(Module.from_dict(module_data))
        return semester

    def __repr__(self):
        return f"Semester(number={self.number}, modules={self.modules})"

class StudyProgram:
    """
    Class representing a study program.
    """
    def __init__(self, name: str, regular_study_period: int = 6):
        self.name = name
        self.regular_study_period = regular_study_period
        self.semesters: List[Semester] = []

    def get_progress(self) -> float:
        """
        Calculate the progress of the study program based on completed ECTS.
        """
        passed_ects = 0
        total_ects = 0
        for semester in self.semesters:
            for module in semester.get_modules():
                total_ects += module.ects
                if module.status == ModuleStatus.PASSED:
                    passed_ects += module.ects
        return (passed_ects / total_ects) * 100 if total_ects > 0 else 0
    
    def to_dict(self) -> dict:
        """
        Convert the study program to a dictionary representation.
        """
        return {
            "name": self.name,
            "regular_study_period": self.regular_study_period,
            "semesters": [semester.to_dict() for semester in self.semesters]
        }

    @staticmethod  
    def from_dict(data: dict):
        """
        Create a StudyProgram instance from a dictionary representation.
        """
        study_program = StudyProgram(
            name=data["name"],
            regular_study_period=data["regular_study_period"]
        )
        for semester_data in data.get("semesters", []):
            study_program.semesters.append(Semester.from_dict(semester_data))
        return study_program

    def __repr__(self):
        return f"StudyProgram(name={self.name}, semesters={self.semesters}, regular_study_period={self.regular_study_period})"