class Student:
    def __init__(self, student_id, name, education_level, skills, interests, goals):
        self.student_id = student_id
        self.name = name
        self.education_level = education_level
        self.skills = skills  # List of skill strings
        self.interests = interests  # List of interest strings
        self.goals = goals  # Career goals
        
    def to_dict(self):
        return {
            'student_id': self.student_id,
            'name': self.name,
            'education_level': self.education_level,
            'skills': self.skills,
            'interests': self.interests,
            'goals': self.goals
        }
    
    def get_skill_vector(self, all_skills):
        """Convert skills to binary vector"""
        return [1 if skill in self.skills else 0 for skill in all_skills]