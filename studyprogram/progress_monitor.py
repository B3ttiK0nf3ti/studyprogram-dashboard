from classes import ModuleStatus

class ProgressMonitor:
    def __init__(self, study_program):
        self.study_program = study_program

    def calc_grade_average(self) -> float:
        """
        Calculate the average grade of all exam performances in the study program.
        """
        total_grade = 0
        count = 0
        for semester in self.study_program.semesters:
            for module in semester.modules:
                for exam in module.exam_performances:
                    if exam.passed:
                        total_grade += exam.grade
                        count += 1
        return total_grade / count if count > 0 else 0
    
    def calc_pass_quote(self) -> float:
        """
        Calculate the pass quote of the study program.
        """
        total_modules = 0
        passed_modules = 0
        for semester in self.study_program.semesters:
            for module in semester.modules:
                total_modules += 1
                if any(ep.is_passed() for ep in module.exam_performances):
                    passed_modules += 1
        return (passed_modules / total_modules) * 100 if total_modules > 0 else 0
    
    def calc_study_progress(self) -> float:
        """
        Calculate the study progress of the study program based on completed ECTS.
        """
        total_ects = 0
        completed_ects = 0
        for semester in self.study_program.semesters:
            for module in semester.modules:
                total_ects += module.ects
                if module.status == ModuleStatus.PASSED:
                    completed_ects += module.ects
        return (completed_ects / total_ects) * 100 if total_ects > 0 else 0
    
    def calc_average_learning_time(self) -> float:
        """
        Calculate the average learning time for all modules in the study program.
        """
        total_learning_time = 0
        count = 0
        for semester in self.study_program.semesters:
            for module in semester.modules:
                for learning_time in module.learning_times:
                    total_learning_time += learning_time.hours
                    count += 1
        return total_learning_time / count if count > 0 else 0