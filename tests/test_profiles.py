import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.student import Student
from services.profile_manager import ProfileManager
from services.nlp_processor import NLPProcessor

class TestProfileManagement(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.profile_manager = ProfileManager()
        self.nlp_processor = NLPProcessor()
        
    def test_create_student_profile(self):
        """Test creating a new student profile"""
        student = self.profile_manager.create_student_profile(
            student_id=1,
            name="John Doe",
            education_level="Bachelor",
            skills=["python", "java"],
            interests=["programming", "technology"],
            goals="Become a software engineer"
        )
        
        self.assertIsNotNone(student)
        self.assertEqual(student.student_id, 1)
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(len(student.skills), 2)
    
    def test_profile_retrieval(self):
        """Test retrieving student profile"""
        # Create a student first
        self.profile_manager.create_student_profile(
            student_id=2,
            name="Jane Smith",
            education_level="Master",
            skills=["python", "machine_learning"],
            interests=["ai", "research"],
            goals="Become an AI researcher"
        )
        
        # Retrieve the student
        student = self.profile_manager.get_student(2)
        self.assertIsNotNone(student)
        self.assertEqual(student.name, "Jane Smith")
    
    def test_update_student_skills(self):
        """Test updating student skills"""
        student = self.profile_manager.create_student_profile(
            student_id=3,
            name="Test User",
            education_level="Bachelor",
            skills=["python"],
            interests=["tech"],
            goals="Test"
        )
        
        new_skills = ["python", "sql", "javascript"]
        success = self.profile_manager.update_student_skills(3, new_skills)
        
        self.assertTrue(success)
        updated_student = self.profile_manager.get_student(3)
        self.assertEqual(len(updated_student.skills), 3)
        self.assertIn("sql", updated_student.skills)
    
    def test_profile_analysis(self):
        """Test student profile analysis"""
        student = self.profile_manager.create_student_profile(
            student_id=4,
            name="Analysis Test",
            education_level="Bachelor",
            skills=["python", "sql"],
            interests=["data", "tech"],
            goals="Test analysis"
        )
        
        analysis = self.profile_manager.analyze_student_profile(student)
        
        self.assertIn('total_skills', analysis)
        self.assertIn('total_interests', analysis)
        self.assertIn('profile_completeness', analysis)
        self.assertEqual(analysis['total_skills'], 2)
        self.assertEqual(analysis['total_interests'], 2)
    
    def test_sentiment_analysis(self):
        """Test NLP sentiment analysis"""
        positive_feedback = "I love this career recommendation system!"
        negative_feedback = "This system is terrible and not helpful."
        neutral_feedback = "The system works okay."
        
        pos_result = self.nlp_processor.analyze_feedback_sentiment(positive_feedback)
        neg_result = self.nlp_processor.analyze_feedback_sentiment(negative_feedback)
        neutral_result = self.nlp_processor.analyze_feedback_sentiment(neutral_feedback)
        
        self.assertEqual(pos_result['sentiment'], 'positive')
        self.assertEqual(neg_result['sentiment'], 'negative')
        self.assertEqual(neutral_result['sentiment'], 'neutral')

if __name__ == '__main__':
    unittest.main()
    