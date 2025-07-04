class ProgressMonitor:
    def __init__(self, study_program):
        self.study_program = study_program

    def calc_grade_average(self) -> float:
        grades = []
        for semester in self.study_program.semesters:
            for module in semester.getModules():
                grade = module.getGrade()
                if grade > 0:
                    grades.append(grade)
        return sum(grades) / len(grades) if grades else 0.0

    def calc_pass_quote(self) -> float:
        total = 0
        passed = 0
        for semester in self.study_program.semesters:
            for module in semester.getModules():
                total += 1
                if module.status == "PASSED":
                    passed += 1
        return (passed / total) * 100 if total > 0 else 0.0

    def calc_study_progress(self) -> float:
        return self.study_program.getProgress()

    def calc_average_learning_time(self) -> float:
        total_hours = 0
        total_entries = 0
        for semester in self.study_program.semesters:
            for module in semester.getModules():
                for lt in module.learning_times:
                    total_hours += lt.getLearningTime()
                    total_entries += 1
        return total_hours / total_entries if total_entries > 0 else 0.0

# class ProgressMonitor:
#     def __init__(self, study_program):
#         self.study_program = study_program

#     def calcGradeAverage(self) -> float:
#         """
#         Calculate the average grade of all exam performances in the study program.
#         """
#         total_grade = 0
#         count = 0
#         for semester in self.study_program.semesters:
#             for module in semester.modules:
#                 for exam in module.exam_performances:
#                     if exam.passed:
#                         total_grade += exam.grade
#                         count += 1
#         return total_grade / count if count > 0 else 0
    
#     def calcPassQuote(self) -> float:
#         """
#         Calculate the pass quote of the study program.
#         """
#         total_modules = 0
#         passed_modules = 0
#         for semester in self.study_program.semesters:
#             for module in semester.modules:
#                 total_modules += 1
#                 if module.exam_performance and module.exam_performance.passed:
#                     passed_modules += 1
#         return (passed_modules / total_modules) * 100 if total_modules > 0 else 0
    
#     def calcStudyProgress(self) -> float:
#         """
#         Calculate the study progress of the study program based on completed ECTS.
#         """
#         total_ects = 0
#         completed_ects = 0
#         for semester in self.study_program.semesters:
#             for module in semester.modules:
#                 total_ects += module.ects
#                 if module.status == ModuleStatus.PASSED:
#                     completed_ects += module.ects
#         return (completed_ects / total_ects) * 100 if total_ects > 0 else 0
    
#     def calcAverageLearningTime(self) -> float:
#         """
#         Calculate the average learning time for all modules in the study program.
#         """
#         total_learning_time = 0
#         count = 0
#         for semester in self.study_program.semesters:
#             for module in semester.modules:
#                 for learning_time in module.learning_times:
#                     total_learning_time += learning_time.hours
#                     count += 1
#         return total_learning_time / count if count > 0 else 0