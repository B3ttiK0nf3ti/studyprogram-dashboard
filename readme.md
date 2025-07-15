# Study Program Tracker (Python)

This project is an object-oriented Python system for managing and analyzing a study program. It allows tracking semesters, modules, exam performances, and learning times.

---

## Features

- Manage modules with ECTS, grades, status, and study times
- Save and restore data as dictionaries (e.g., for JSON files)
- Calculate average grades per module
- Calculate overall study progress based on passed modules
- Fully object-oriented design using Python classes and enums

---

## Classes Overview

### `ModuleStatus` (Enum)
Represents the status of a module:
- `OPEN`
- `PASSED`
- `FAILED`

---

### `ExamPerformance`
Represents a student's exam result.
- Attributes: `grade`, `attempt`, `passed`
- Methods: `is_passed()`

---

### `LearningTime`
Represents study time for a module.
- Attributes: `date`, `hours`
- Methods: `get_learning_time()`

---

### `Module`
Represents a course module.
- Attributes: `title`, `ects`, `status`, `exam_performances`, `learning_times`
- Methods:
  - `get_grade()` – Calculate average grade
  - `to_dict()` / `from_dict()` – Convert to/from dictionary (e.g., for JSON)
  - `add_exam_performance()` – Add an exam performance
  - `add_learning_time()` – Add a learning time entry

---

### `Semester`
Represents a semester in the study program.
- Attributes: `number`, `modules`
- Methods:
  - `add_module()` – Add a module to the semester
  - `get_modules()` – Get list of modules
  - `to_dict()` / `from_dict()` – Serialization helpers

---

### `StudyProgram`
Represents the complete study program.
- Attributes: `name`, `regular_study_period`, `semesters`
- Methods:
  - `get_progress()` – Calculates overall ECTS progress
  - `to_dict()` / `from_dict()` – Save/load from structured format

---

### `DataManger`
Handles loading/saving JSON data.
- Attributes: `file_path`
- Methods:
  - `save_data(data: dict)` – save data
  - `load_data()` – load data

---

### `ProgressMonitor`
Provides analytics.
- Attributes: `study_program`
- Methods:
  - `calc_grade_average()` – calculates average grade
  - `calc_pass_quote()` – calculates the success rate
  - `calc_study_progress()` - calculates the study progress
  - `calc_average_learning_time()` - calculates average learning tim

---

### `CLIController`
Manages all user input/output interactions in the terminal.
Handles user prompts and actions
Interacts with DataManager, StudyProgram, ProgressMonitor

---

### `SetupController`
Initializes dependencies and creates the CLI controller.
Loads existing JSON data (or creates new StudyProgram)
Injects all dependencies into CLIController

## Example Data Format

### Example output of `Module.to_dict()`:

json
{
  "title": "Mathematics I",
  "ects": 5,
  "status": "passed",
  "exam_performances": [
    {"grade": 1.7, "attempt": 1, "passed": true}
  ],
  "learning_times": [
    {"date": "2024-05-10", "hours": 3.5}
  ]
}


## DataManager

The `DataManager` class handles reading and writing study program data to a JSON file.

### Purpose

It ensures data persistence by saving and loading program data from disk.

### Class: `DataManager`

python
data_manager = DataManager("study_data.json")

## ProgressMonitor

The `ProgressMonitor` class provides analytical methods for evaluating a student's academic progress in a study program.

### Purpose

This class is responsible for calculating metrics such as:
- Average grade
- Module pass rate
- ECTS-based study progress
- Average learning time

---

### Class: `ProgressMonitor`

python
monitor = ProgressMonitor(study_program)

# Study Progress Tracker CLI

A terminal-based application to track study progress, manage modules, record exam performances, log learning time, and visualize analytics directly in the terminal.

---

## Overview

This project helps students manage their study program by:

- Adding and managing modules per semester
- Logging grades with attempt tracking
- Recording and analyzing learning time
- Viewing terminal-based dashboards and statistics
- Saving/loading progress via JSON

---

## Features

- Add/edit/delete modules per semester
- Track grades with max 3 attempts per module
- Log study hours for each module
- Visual dashboard with:
  - Grade trend over semesters
  - Learning time (planned vs. actual)
  - ECTS-based study progress
  - Exam status: Open, Passed, Failed

---

## Technologies

- Python 3.9+
- [`plotext`](https://pypi.org/project/plotext/) for terminal plots
- `json` for data persistence

---

## Folder Structure
studyprogram/
│
├── main.py                # Entry point – runs CLI
├── setup_controller.py    # Creates & wires all components
├── cli_controller.py      # Terminal UI logic
├── progress_monitor.py    # Analytics logic
├── data_manager.py        # Save/load JSON
├── classes.py             # All data models and enums
├── study_data.json        # Data storage (auto-generated)
└── README.md              # Project documentation

