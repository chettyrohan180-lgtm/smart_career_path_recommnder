import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

class NLPProcessor:
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        print("✅ NLP Processor initialized successfully (NLTK only)")
    
    def analyze_feedback_sentiment(self, feedback_text):
        """Analyze sentiment of user feedback using NLTK"""
        try:
            scores = self.sentiment_analyzer.polarity_scores(feedback_text)
            
            if scores['compound'] >= 0.05:
                sentiment = 'positive'
            elif scores['compound'] <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
                
            return {
                'sentiment': sentiment,
                'scores': scores
            }
        except Exception as e:
            return {
                'sentiment': 'neutral',
                'scores': {'compound': 0, 'pos': 0, 'neg': 0, 'neu': 1},
                'error': str(e)
            }
    
    def extract_skills_from_text(self, text):
        """Extract potential skills from text using keyword matching"""
        try:
            skills = []
            
            # Comprehensive skill list
            technical_terms = [
                'python', 'java', 'javascript', 'sql', 'machine learning', 
                'data analysis', 'aws', 'docker', 'kubernetes', 'react',
                'html', 'css', 'statistics', 'excel', 'tableau', 'powerbi',
                'deep learning', 'ai', 'artificial intelligence', 'data science',
                'web development', 'software engineering', 'cloud computing',
                'linux', 'windows', 'macos', 'git', 'github', 'agile', 'scrum',
                'project management', 'communication', 'teamwork', 'leadership',
                'problem solving', 'analytical thinking', 'creativity'
            ]
            
            text_lower = text.lower()
            for skill in technical_terms:
                if skill in text_lower and skill not in skills:
                    skills.append(skill)
                    
            return skills
        except Exception as e:
            print(f"Error extracting skills: {e}")
            return []
    
    def calculate_text_similarity(self, text1, text2):
        """Calculate similarity between two texts using word overlap"""
        try:
            if not text1 or not text2:
                return 0.0
                
            # Clean and split texts
            words1 = set(re.findall(r'\b\w+\b', text1.lower()))
            words2 = set(re.findall(r'\b\w+\b', text2.lower()))
            
            if not words1 or not words2:
                return 0.0
                
            intersection = words1.intersection(words2)
            union = words1.union(words2)
            
            return len(intersection) / len(union) if union else 0.0
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0