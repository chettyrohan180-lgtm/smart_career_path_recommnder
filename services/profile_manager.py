from models.student import Student

class ProfileManager:
    def __init__(self):
        self.students = {}
        
    def create_student_profile(self, student_id, name, education_level, skills, interests, goals):
        """Create a new student profile"""
        student = Student(student_id, name, education_level, skills, interests, goals)
        self.students[student_id] = student
        return student
    
    def get_student(self, student_id):
        """Retrieve student profile"""
        return self.students.get(student_id)
    
    def update_student_skills(self, student_id, new_skills):
        """Update student skills"""
        if student_id in self.students:
            self.students[student_id].skills = new_skills
            return True
        return False
    
    def analyze_student_profile(self, student):
        """Analyze student profile completeness"""
        analysis = {
            'total_skills': len(student.skills),
            'total_interests': len(student.interests),
            'has_goals': bool(student.goals),
            'profile_completeness': 0
        }
        
        completeness_score = 0
        if student.skills: completeness_score += 40
        if student.interests: completeness_score += 30
        if student.goals: completeness_score += 30
        
        analysis['profile_completeness'] = completeness_score
        return analysis