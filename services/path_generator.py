import pandas as pd

class PathGenerator:
    def __init__(self, careers_data_path):
        self.careers_df = pd.read_csv(careers_data_path)
        
    def generate_learning_path(self, student, target_career, timeframe_months=12):
        """Generate personalized learning path to target career"""
        career_data = self.careers_df[
            self.careers_df['career_title'] == target_career
        ]
        
        if career_data.empty:
            return None
            
        career = career_data.iloc[0]
        required_skills = career['required_skills'].split(',')
        current_skills = student.skills
        
        # Identify skill gaps
        skill_gaps = [skill for skill in required_skills if skill not in current_skills]
        
        # Generate learning path
        learning_path = {
            'target_career': target_career,
            'current_skills_match': f"{len([s for s in required_skills if s in current_skills])}/{len(required_skills)}",
            'skill_gaps': skill_gaps,
            'timeline_months': timeframe_months,
            'learning_phases': [],
            'resources': self._get_learning_resources(skill_gaps)
        }
        
        # Create phased learning plan
        phases = self._create_learning_phases(skill_gaps, timeframe_months)
        learning_path['learning_phases'] = phases
        
        return learning_path
    
    def _create_learning_phases(self, skill_gaps, total_months):
        """Create phased learning plan"""
        if not skill_gaps:
            return []
            
        phases = []
        skills_per_phase = max(1, len(skill_gaps) // 3)
        
        for i in range(0, len(skill_gaps), skills_per_phase):
            phase_skills = skill_gaps[i:i + skills_per_phase]
            phase_duration = max(1, total_months // ((len(skill_gaps) // skills_per_phase) + 1))
            
            phase = {
                'phase_name': f'Phase {len(phases) + 1}',
                'duration_weeks': phase_duration * 4,
                'skills_to_learn': phase_skills,
                'milestones': [f"Complete {skill} fundamentals" for skill in phase_skills]
            }
            phases.append(phase)
            
        return phases
    
    def _get_learning_resources(self, skills):
        """Get learning resources for skills"""
        resource_map = {
            'python': ['Python.org tutorial', 'Codecademy Python', 'Real Python articles'],
            'machine_learning': ['Coursera ML course', 'Fast.ai', 'Kaggle tutorials'],
            'sql': ['SQLZoo', 'Mode Analytics SQL tutorial', 'LeetCode SQL problems'],
            'javascript': ['MDN JavaScript guide', 'FreeCodeCamp JavaScript', 'Eloquent JavaScript'],
            'aws': ['AWS Training', 'AWS Whitepapers', 'Cloud Guru courses'],
            'data_analysis': ['DataCamp', 'Towards Data Science', 'Kaggle notebooks'],
            'java': ['Oracle Java Tutorials', 'Codecademy Java', 'Java for Beginners'],
            'react': ['React Official Tutorial', 'FreeCodeCamp React', 'React Documentation'],
            'docker': ['Docker Getting Started', 'Docker Documentation', 'Docker Tutorials'],
            'kubernetes': ['Kubernetes Basics', 'K8s Documentation', 'Kubernetes Tutorials'],
            'statistics': ['Khan Academy Statistics', 'Coursera Statistics', 'StatQuest YouTube'],
            'tableau': ['Tableau Training', 'Tableau Tutorials', 'Tableau Public Gallery'],
            'excel': ['Microsoft Excel Help', 'Excel Easy', 'Chandoo Excel Tutorials']
        }
        
        resources = {}
        for skill in skills:
            resources[skill] = resource_map.get(skill, ['Online tutorials', 'Documentation', 'Practice projects'])
            
        return resources