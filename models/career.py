class Career:
    def __init__(self, career_id, title, required_skills, preferred_skills, industry, growth_potential, salary_range, education_level):
        self.career_id = career_id
        self.title = title
        self.required_skills = required_skills
        self.preferred_skills = preferred_skills
        self.industry = industry
        self.growth_potential = growth_potential
        self.salary_range = salary_range
        self.education_level = education_level
        
    def to_dict(self):
        return {
            'career_id': self.career_id,
            'title': self.title,
            'required_skills': self.required_skills,
            'preferred_skills': self.preferred_skills,
            'industry': self.industry,
            'growth_potential': self.growth_potential,
            'salary_range': self.salary_range,
            'education_level': self.education_level
        }
    
    def get_skill_vector(self, all_skills):
        """Convert required skills to binary vector"""
        return [1 if skill in self.required_skills else 0 for skill in all_skills]