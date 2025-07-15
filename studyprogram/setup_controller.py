from classes import StudyProgram
from progress_monitor import ProgressMonitor
from data_manager import DataManager
from cli_controller import CLIController

class SetupController:
    def __init__(self, file_path="study_data.json"):
        # Initialize DataManager to handle loading/saving data
        self.data_manager = DataManager(file_path)

        # Load existing study program from file, or create a new one if none exists
        self.study_program = self._load_or_create_study_program()

        # Initialize the progress monitor with the loaded or new study program
        self.progress_monitor = ProgressMonitor(self.study_program)

    def _load_or_create_study_program(self) -> StudyProgram:
        # Try to load data from JSON file
        data = self.data_manager.load_data()

        # If data was loaded successfully, recreate the StudyProgram object from it
        if data:
            return StudyProgram.from_dict(data)

        # Otherwise, create a new default study program
        return StudyProgram(name="Softwareentwicklung", regular_study_period=6)

    def create_controller(self) -> CLIController:
        # Return a fully configured CLIController with all necessary components
        return CLIController(
            data_manager=self.data_manager,
            study_program=self.study_program,
            progress_monitor=self.progress_monitor
        )
