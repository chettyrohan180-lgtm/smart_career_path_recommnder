import pandas as pd
from models.recommender_model import CareerRecommender

class CareerMatcher:
    def __init__(self, careers_data_path):
        self.careers_df = pd.read_csv(careers_data_path)
        self.recommender = CareerRecommender()
        self.recommender.load_data(self.careers_df)
        
    def find_career_matches(self, student, top_n=5):
        """Find career matches for a student"""
        recommendations = self.recommender.recommend_careers(
            student.skills, student.interests, top_n
        )
        
        # Add education compatibility
        for rec in recommendations:
            education_score = self._calculate_education_compatibility(
                student.education_level, rec['education_level']
            )
            rec['education_compatibility'] = education_score
            rec['overall_score'] = (
                rec['similarity_score'] * 0.4 +
                (rec['skill_match_percentage'] / 100) * 0.3 +
                education_score * 0.3
            )
            
        # Sort by overall score
        recommendations.sort(key=lambda x: x['overall_score'], reverse=True)
        return recommendations
    
    def _calculate_education_compatibility(self, student_edu, career_edu):
        """Calculate education level compatibility"""
        education_levels = {
            'High School': 1,
            'Associate': 2,
            'Bachelor': 3,
            'Master': 4,
            'PhD': 5
        }
        
        student_level = education_levels.get(student_edu, 0)
        career_level = education_levels.get(career_edu, 0)
        
        if student_level >= career_level:
            return 1.0
        else:
            return max(0.1, 1 - (career_level - student_level) * 0.2)
    
    def get_career_details(self, career_title):
        """Get detailed information about a specific career"""
        career = self.careers_df[self.careers_df['career_title'] == career_title]
        if not career.empty:
            return career.iloc[0].to_dict()
        return None