import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class CareerVisualizer:
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        
    def plot_recommendation_scores(self, recommendations, student_name):
        """Plot recommendation scores for a student"""
        if not recommendations:
            print("No recommendations to visualize")
            return
            
        careers = [rec['career'] for rec in recommendations]
        overall_scores = [rec['overall_score'] for rec in recommendations]
        skill_matches = [rec['skill_match_percentage'] for rec in recommendations]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Overall scores
        ax1.barh(careers, overall_scores, color='skyblue')
        ax1.set_xlabel('Overall Score')
        ax1.set_title(f'Career Recommendations for {student_name}')
        ax1.set_xlim(0, 1)
        
        # Skill match percentages
        ax2.barh(careers, skill_matches, color='lightgreen')
        ax2.set_xlabel('Skill Match (%)')
        ax2.set_title('Skill Compatibility')
        ax2.set_xlim(0, 100)
        
        plt.tight_layout()
        plt.show()
    
    def plot_skill_gaps(self, learning_path):
        """Visualize skill gaps for a learning path"""
        if not learning_path or 'skill_gaps' not in learning_path:
            print("No skill gap data to visualize")
            return
            
        skill_gaps = learning_path['skill_gaps']
        
        if not skill_gaps:
            print("No skill gaps identified!")
            return
            
        plt.figure(figsize=(10, 6))
        y_pos = range(len(skill_gaps))
        
        plt.barh(y_pos, [1] * len(skill_gaps), color='red', alpha=0.7)
        plt.yticks(y_pos, skill_gaps)
        plt.xlabel('Skills to Learn')
        plt.title(f"Skill Gaps for {learning_path['target_career']}")
        plt.tight_layout()
        plt.show()
    
    def plot_career_distribution(self, careers_df):
        """Plot distribution of careers by industry and growth potential"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Industry distribution
        industry_counts = careers_df['industry'].value_counts()
        ax1.pie(industry_counts.values, labels=industry_counts.index, autopct='%1.1f%%')
        ax1.set_title('Career Distribution by Industry')
        
        # Growth potential distribution
        growth_counts = careers_df['growth_potential'].value_counts()
        sns.barplot(x=growth_counts.index, y=growth_counts.values, ax=ax2, palette='viridis')
        ax2.set_title('Career Distribution by Growth Potential')
        ax2.set_ylabel('Number of Careers')
        
        plt.tight_layout()
        plt.show()