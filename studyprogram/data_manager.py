import json

class DataManager:
    """
    Class to manage data loading and saving for the study program.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    @staticmethod
    def save_data(data, file_path: str):
        """
        Save data to a JSON file.
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def load_data(file_path: str):
        """
        Load data from a JSON file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {file_path}.")
            return None

    def serialize_object(self, obj) -> dict:
        return obj.to_dict()

    def deserialize_object(self, data: dict, module_class):
        return module_class.from_dict(data)