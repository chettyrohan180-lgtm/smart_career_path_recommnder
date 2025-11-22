import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.student import Student
from services.career_matcher import CareerMatcher
from services.profile_manager import ProfileManager

class TestCareerMatching(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.career_matcher = CareerMatcher('data/careers.csv')
        self.profile_manager = ProfileManager()
        
        # Create test student
        self.test_student = self.profile_manager.create_student_profile(
            student_id=100,
            name="Test Student",
            education_level="Bachelor",
            skills=["python", "sql", "data_analysis"],
            interests=["technology", "data_science"],
            goals="Become a data professional"
        )
    
    def test_student_creation(self):
        """Test that student profile is created correctly"""
        self.assertEqual(self.test_student.name, "Test Student")
        self.assertEqual(self.test_student.education_level, "Bachelor")
        self.assertIn("python", self.test_student.skills)
    
    def test_career_recommendations(self):
        """Test that career recommendations are generated"""
        recommendations = self.career_matcher.find_career_matches(self.test_student, top_n=3)
        
        self.assertIsNotNone(recommendations)
        self.assertLessEqual(len(recommendations), 3)
        
        # Check structure of recommendations
        for rec in recommendations:
            self.assertIn('career', rec)
            self.assertIn('similarity_score', rec)
            self.assertIn('skill_match_percentage', rec)
            self.assertIn('overall_score', rec)
    
    def test_education_compatibility(self):
        """Test education compatibility calculation"""
        # Test case where student has sufficient education
        score1 = self.career_matcher._calculate_education_compatibility("Master", "Bachelor")
        self.assertEqual(score1, 1.0)
        
        # Test case where student needs more education
        score2 = self.career_matcher._calculate_education_compatibility("Bachelor", "Master")
        self.assertLess(score2, 1.0)
    
    def test_recommendation_scores_range(self):
        """Test that recommendation scores are within valid range"""
        recommendations = self.career_matcher.find_career_matches(self.test_student, top_n=5)
        
        for rec in recommendations:
            self.assertGreaterEqual(rec['overall_score'], 0)
            self.assertLessEqual(rec['overall_score'], 1)
            self.assertGreaterEqual(rec['skill_match_percentage'], 0)
            self.assertLessEqual(rec['skill_match_percentage'], 100)

if __name__ == '__main__':
    unittest.main()