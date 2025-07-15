import json
from classes import StudyProgram, Semester, Module, ExamPerformance, LearningTime, ModuleStatus
from datetime import date

# 1. create a test study program
def create_test_study_program():
    program = StudyProgram(name="Testprogramm", regular_study_period=6)
    
    semester = Semester(number=1)
    module = Module(title="Mathematik", ects=5, status=ModuleStatus.PASSED)
    module.add_exam_performance(ExamPerformance(grade=1.7, attempt=1, passed=True))
    module.add_learning_time(LearningTime(date=date.today(), hours=3.5))

    semester.add_module(module)
    program.semesters.append(semester)

    return program

# 2. serialization
def serialize_program(program: StudyProgram) -> str:
    as_dict = program.to_dict()
    return json.dumps(as_dict, indent=4)

# 3. deserialization
def deserialize_program(json_str: str) -> StudyProgram:
    loaded_dict = json.loads(json_str)
    return StudyProgram.from_dict(loaded_dict)

# 4. Roundtrip Test
def test_serialization_roundtrip():
    original = create_test_study_program()
    json_data = serialize_program(original)
    reconstructed = deserialize_program(json_data)

    # debug output
    print("Original:", original)
    print("JSON:", json_data)
    print("Reconstructed:", reconstructed)

    # Assertions to verify correctness
    assert original.name == reconstructed.name
    assert original.semesters[0].modules[0].title == reconstructed.semesters[0].modules[0].title
    assert original.semesters[0].modules[0].exam_performances[0].grade == reconstructed.semesters[0].modules[0].exam_performances[0].grade

    print("Roundtrip-Test successful!")

# run the test
if __name__ == "__main__":
    test_serialization_roundtrip()
