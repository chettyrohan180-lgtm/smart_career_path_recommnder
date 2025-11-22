import pandas as pd
import json
import os

class DataLoader:
    def __init__(self, data_directory='data'):
        self.data_directory = data_directory
        
    def load_careers_data(self, filename='careers.csv'):
        """Load careers data from CSV"""
        filepath = os.path.join(self.data_directory, filename)
        try:
            df = pd.read_csv(filepath)
            print(f"Loaded {len(df)} careers from {filename}")
            return df
        except FileNotFoundError:
            print(f"Career data file not found: {filepath}")
            return pd.DataFrame()
    
    def load_skills_mapping(self, filename='skills_mapping.json'):
        """Load skills mapping from JSON"""
        filepath = os.path.join(self.data_directory, filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Skills mapping file not found: {filepath}")
            return {}
    
    def save_student_data(self, students_data, filename='students.json'):
        """Save student data to JSON"""
        filepath = os.path.join(self.data_directory, filename)
        with open(filepath, 'w') as f:
            json.dump(students_data, f, indent=2)
    
    def load_student_data(self, filename='students.json'):
        """Load student data from JSON"""
        filepath = os.path.join(self.data_directory, filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}   