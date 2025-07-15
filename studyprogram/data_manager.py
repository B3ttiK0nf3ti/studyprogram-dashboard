import json

class DataManager:
    """
    Class to manage data loading and saving for the study program.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def save_data(self, data):
        """
        Save data to a JSON file.
        """
        with open(self.file_path, "w", encoding="utf-8") as file:  
            json.dump(data, file, indent=4)
        print(f"File {self.file_path} saved.")  

    def load_data(self):
        """
        Load data from a JSON file.
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:  
                data = json.load(file)
            print(f"File {self.file_path} loaded.")  
            return data
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")  
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {self.file_path}.") 
            return None

