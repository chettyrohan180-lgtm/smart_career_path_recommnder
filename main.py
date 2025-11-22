import pandas as pd
from services.profile_manager import ProfileManager
from services.career_matcher import CareerMatcher
from services.path_generator import PathGenerator
from services.nlp_processor import NLPProcessor
from utils.visualizer import CareerVisualizer
from utils.data_loader import DataLoader

class CareerRecommenderSystem:
    def __init__(self):
        self.profile_manager = ProfileManager()
        self.career_matcher = CareerMatcher('data/careers.csv')
        self.path_generator = PathGenerator('data/careers.csv')
        self.nlp_processor = NLPProcessor()
        self.visualizer = CareerVisualizer()
        self.data_loader = DataLoader()
    
    def get_user_input(self):
        """Get student information from user input"""
        print("Smart Career Path Recommender System")
        print("=" * 50)
        print("Please enter your information:\n")
        
        # Get basic information
        name = input("Enter your name: ")
        
        print("\nEducation Level Options:")
        print("1. High School")
        print("2. Bachelor's Degree") 
        print("3. Master's Degree")
        print("4. PhD")
        edu_choice = input("Select your education level (1-4): ")
        
        education_map = {
            "1": "High School",
            "2": "Bachelor", 
            "3": "Master",
            "4": "PhD"
        }
        education_level = education_map.get(edu_choice, "Bachelor")
        
        # Get skills
        print("\nAvailable Skills (enter numbers separated by commas):")
        available_skills = [
            "python", "java", "javascript", "sql", "html", "css",
            "machine_learning", "data_analysis", "statistics", "excel",
            "aws", "docker", "kubernetes", "react", "tableau", "powerbi",
            "project_management", "communication", "leadership", "problem_solving"
        ]
        
        for i, skill in enumerate(available_skills, 1):
            print(f"{i}. {skill}")
        
        skill_choices = input("\nSelect your skills (e.g., 1,3,5): ")
        selected_skills = []
        for choice in skill_choices.split(','):
            choice = choice.strip()
            if choice.isdigit() and 1 <= int(choice) <= len(available_skills):
                selected_skills.append(available_skills[int(choice) - 1])
        
        # Get interests
        print("\nInterest Areas (enter numbers separated by commas):")
        interest_areas = [
            "technology", "data_science", "web_development", "artificial_intelligence",
            "business", "design", "research", "healthcare", "education", "finance",
            "gaming", "entrepreneurship", "cybersecurity", "cloud_computing"
        ]
        
        for i, interest in enumerate(interest_areas, 1):
            print(f"{i}. {interest}")
        
        interest_choices = input("\nSelect your interests (e.g., 1,2,3): ")
        selected_interests = []
        for choice in interest_choices.split(','):
            choice = choice.strip()
            if choice.isdigit() and 1 <= int(choice) <= len(interest_areas):
                selected_interests.append(interest_areas[int(choice) - 1])
        
        # Get career goals with options
        print("\nCareer Goal Options:")
        career_goals = [
            "Become a software developer/engineer",
            "Pursue a career in data science/analysis",
            "Work in artificial intelligence/machine learning",
            "Become a web developer/frontend specialist",
            "Pursue cloud computing/DevOps roles",
            "Work in cybersecurity",
            "Become a product/project manager",
            "Pursue UX/UI design career",
            "Start my own tech business",
            "Work in research and development",
            "Other (custom goal)"
        ]
        
        for i, goal in enumerate(career_goals, 1):
            print(f"{i}. {goal}")
        
        goal_choice = input("\nSelect your primary career goal (1-11): ")
        
        if goal_choice.isdigit() and 1 <= int(goal_choice) <= len(career_goals):
            if int(goal_choice) == 11:
                custom_goal = input("Enter your custom career goal: ")
                goals = custom_goal
            else:
                goals = career_goals[int(goal_choice) - 1]
        else:
            goals = "Explore suitable career paths"
        
        return name, education_level, selected_skills, selected_interests, goals
    
    def run_interactive_system(self):
        """Run the interactive career recommender"""
        print("Smart Career Path Recommender System")
        print("=" * 50)
        
        # Get user input
        name, education_level, skills, interests, goals = self.get_user_input()
        
        # Create student profile
        student = self.profile_manager.create_student_profile(
            student_id=1,
            name=name,
            education_level=education_level,
            skills=skills,
            interests=interests,
            goals=goals
        )
        
        print(f"\n Profile created for: {student.name}")
        print(f"   Education: {student.education_level}")
        print(f"   Skills: {', '.join(student.skills)}")
        print(f"   Interests: {', '.join(student.interests)}")
        print(f"   Goals: {student.goals}")
        
        # Get career recommendations
        print("\n Analyzing your profile and finding career matches...")
        recommendations = self.career_matcher.find_career_matches(student, top_n=5)
        
        print("\n Top Career Recommendations for You:")
        print("=" * 40)
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec['career']}")
            print(f"    Overall Score: {rec['overall_score']:.2f}")
            print(f"    Skill Match: {rec['skill_match_percentage']}%")
            print(f"    Growth: {rec['growth_potential']}")
            print(f"    Salary: {rec['salary_range']}")
            print(f"    Education: {rec['education_level']}")
            if rec['missing_skills']:
                print(f"    Skills to learn: {', '.join(rec['missing_skills'])}")
            print()
        
        # Generate learning path for top recommendation
        if recommendations:
            top_career = recommendations[0]['career']
            print(f" Generating learning path for your top career: {top_career}")
            
            learning_path = self.path_generator.generate_learning_path(student, top_career)
            
            if learning_path:
                print(f"\n Your Learning Path for {top_career}:")
                print(f"Current Skills Match: {learning_path['current_skills_match']}")
                print(f"Skill Gaps to Fill: {', '.join(learning_path['skill_gaps'])}")
                
                print("\n Your Learning Plan:")
                for phase in learning_path['learning_phases']:
                    print(f"  {phase['phase_name']} ({phase['duration_weeks']} weeks):")
                    print(f"     Skills: {', '.join(phase['skills_to_learn'])}")
                    print(f"     Milestones: {', '.join(phase['milestones'])}")
                
                print("\n Learning Resources:")
                for skill, resources in learning_path['resources'].items():
                    print(f"  {skill}: {', '.join(resources)}")
        
        # Ask for feedback
        feedback = input("\n How was your experience with our career recommender? ")
        if feedback:
            sentiment = self.nlp_processor.analyze_feedback_sentiment(feedback)
            print(f"   Thank you for your {sentiment['sentiment']} feedback!")
        
        # Visualize results
        print("\n Generating your personalized career report...")
        self.visualizer.plot_recommendation_scores(recommendations, student.name)
        
        if learning_path:
            self.visualizer.plot_skill_gaps(learning_path)
        
        print("\n Career exploration complete! Good luck on your journey!")

if __name__ == "__main__":
    system = CareerRecommenderSystem()
    system.run_interactive_system()