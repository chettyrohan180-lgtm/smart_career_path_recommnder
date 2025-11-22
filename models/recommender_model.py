import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

class CareerRecommender:
    def __init__(self):
        self.careers_df = None
        self.all_skills = []
        self.tfidf_vectorizer = None
        self.similarity_matrix = None
        self.knn_model = None
        
    def load_data(self, careers_df):
        """Load career data and prepare models"""
        self.careers_df = careers_df
        
        # Extract all unique skills
        all_skills_set = set()
        for skills in careers_df['required_skills']:
            all_skills_set.update(skills.split(','))
        for skills in careers_df['preferred_skills']:
            all_skills_set.update(skills.split(','))
            
        self.all_skills = sorted(list(all_skills_set))
        
        # Prepare TF-IDF features
        career_descriptions = [
            f"{row['required_skills']} {row['preferred_skills']} {row['industry']}"
            for _, row in careers_df.iterrows()
        ]
        
        self.tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(career_descriptions)
        
        # Build similarity matrix
        self.similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Train KNN model
        self.knn_model = NearestNeighbors(n_neighbors=5, metric='cosine')
        self.knn_model.fit(tfidf_matrix)
        
    def recommend_careers(self, student_skills, student_interests, top_n=5):
        """Recommend careers based on student profile"""
        if self.careers_df is None:
            raise ValueError("Data not loaded. Call load_data() first.")
            
        # Create student profile vector
        student_profile = ' '.join(student_skills + student_interests)
        student_vector = self.tfidf_vectorizer.transform([student_profile])
        
        # Calculate similarities
        similarities = cosine_similarity(student_vector, self.tfidf_vectorizer.transform([
            f"{row['required_skills']} {row['preferred_skills']} {row['industry']}"
            for _, row in self.careers_df.iterrows()
        ]))
        
        # Get top recommendations
        top_indices = similarities[0].argsort()[-top_n:][::-1]
        
        recommendations = []
        for idx in top_indices:
            career = self.careers_df.iloc[idx]
            score = similarities[0][idx]
            
            # Calculate skill match percentage
            required_skills = career['required_skills'].split(',')
            matched_skills = [skill for skill in required_skills if skill in student_skills]
            skill_match = len(matched_skills) / len(required_skills) if required_skills else 0
            
            recommendations.append({
                'career': career['career_title'],
                'similarity_score': round(score, 3),
                'skill_match_percentage': round(skill_match * 100, 1),
                'industry': career['industry'],
                'growth_potential': career['growth_potential'],
                'salary_range': career['salary_range'],
                'education_level': career['education_level'],
                'missing_skills': [skill for skill in required_skills if skill not in student_skills]
            })
            
        return recommendations