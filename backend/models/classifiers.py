"""
Machine Learning models for ticket classification and analysis
"""
import pickle
import numpy as np
from typing import Tuple, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import os


class CategoryClassifier:
    """Classify tickets into categories"""
    
    CATEGORIES = ['delivery', 'refund', 'payment', 'product_issue', 'order_tracking', 'account', 'other']
    
    def __init__(self, model_path: str = None):
        """Initialize classifier"""
        self.model_path = model_path
        self.label_encoder = LabelEncoder()
        self.model = None
        self.vectorizer = None
        self._build_model()
    
    def _build_model(self):
        """Build the classifier pipeline"""
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, ngram_range=(1, 2))),
            ('classifier', LogisticRegression(max_iter=1000, random_state=42))
        ])
    
    def train(self, texts: list, labels: list):
        """Train the classifier"""
        self.label_encoder.fit(self.CATEGORIES)
        y = self.label_encoder.transform(labels)
        self.model.fit(texts, y)
    
    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict ticket category
        Returns: (category, confidence_score)
        """
        if self.model is None:
            return 'other', 0.0
        
        prediction = self.model.predict([text])[0]
        proba = self.model.predict_proba([text])[0]
        confidence = max(proba)
        
        category = self.label_encoder.inverse_transform([prediction])[0]
        return category, float(confidence)
    
    def predict_batch(self, texts: list) -> list:
        """Predict categories for multiple texts"""
        return [self.predict(text) for text in texts]
    
    def save(self, path: str):
        """Save model to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({'model': self.model, 'encoder': self.label_encoder}, f)
    
    def load(self, path: str):
        """Load model from disk"""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.label_encoder = data['encoder']


class PriorityClassifier:
    """Predict ticket priority"""
    
    PRIORITIES = ['low', 'medium', 'high', 'critical']
    
    def __init__(self, model_path: str = None):
        """Initialize classifier"""
        self.model_path = model_path
        self.label_encoder = LabelEncoder()
        self.model = None
        self._build_model()
    
    def _build_model(self):
        """Build the classifier pipeline"""
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])
    
    def train(self, texts: list, labels: list):
        """Train the classifier"""
        self.label_encoder.fit(self.PRIORITIES)
        y = self.label_encoder.transform(labels)
        self.model.fit(texts, y)
    
    def predict(self, text: str, sentiment: str = None) -> Tuple[str, float]:
        """
        Predict ticket priority (consider sentiment too)
        Returns: (priority, confidence_score)
        """
        if self.model is None:
            return 'medium', 0.5
        
        prediction = self.model.predict([text])[0]
        proba = self.model.predict_proba([text])[0]
        confidence = max(proba)
        
        priority = self.label_encoder.inverse_transform([prediction])[0]
        
        # Boost priority if sentiment is very negative
        if sentiment in ['very_negative', 'negative']:
            priority_values = {'low': 0, 'medium': 1, 'high': 2, 'critical': 3}
            sentiment_boost = {'very_negative': 2, 'negative': 1}
            boosted_value = min(3, priority_values.get(priority, 1) + sentiment_boost.get(sentiment, 0))
            priority = self.PRIORITIES[boosted_value]
        
        return priority, float(confidence)
    
    def save(self, path: str):
        """Save model to disk"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({'model': self.model, 'encoder': self.label_encoder}, f)
    
    def load(self, path: str):
        """Load model from disk"""
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
                self.model = data['model']
                self.label_encoder = data['encoder']


class IntentExtractor:
    """Extract intent from ticket"""
    
    INTENTS = ['complaint', 'request', 'information', 'billing', 'technical_issue']
    
    def __init__(self):
        """Initialize extractor"""
        self.model = None
        self._build_model()
    
    def _build_model(self):
        """Build the intent extraction model"""
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
            ('classifier', LogisticRegression(max_iter=1000, random_state=42))
        ])
    
    def extract_intent(self, text: str) -> dict:
        """Extract intent from ticket text"""
        # Keyword-based intent extraction (can be enhanced with ML)
        text_lower = text.lower()
        
        intents = {
            'complaint': sum(1 for word in ['bad', 'poor', 'terrible', 'awful', 'disappointed', 'angry'] if word in text_lower),
            'request': sum(1 for word in ['please', 'can you', 'would', 'could', 'need', 'want'] if word in text_lower),
            'information': sum(1 for word in ['how', 'what', 'when', 'where', 'why', 'explain'] if word in text_lower),
            'billing': sum(1 for word in ['charge', 'payment', 'bill', 'refund', 'money', 'price'] if word in text_lower),
            'technical_issue': sum(1 for word in ['not working', 'error', 'bug', 'issue', 'problem', 'broken'] if word in text_lower)
        }
        
        # Get the intent with highest score
        primary_intent = max(intents, key=intents.get)
        confidence = intents[primary_intent] / (1 + sum(intents.values()))
        
        return {
            'primary_intent': primary_intent,
            'confidence': min(confidence, 0.95) if intents[primary_intent] > 0 else 0.1,
            'all_intents': intents
        }
