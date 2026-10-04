"""
Utility functions for text preprocessing and NLP
"""
import re
import string
from typing import List, Tuple
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class TextProcessor:
    """Text preprocessing utilities"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        
        # Remove special characters but keep spaces and basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def tokenize(text: str) -> List[str]:
        """Tokenize text"""
        return word_tokenize(text)
    
    @staticmethod
    def remove_stopwords(tokens: List[str], language: str = 'english') -> List[str]:
        """Remove stopwords from tokens"""
        stop_words = set(stopwords.words(language))
        return [token for token in tokens if token.lower() not in stop_words]
    
    @staticmethod
    def extract_entities(text: str) -> dict:
        """Extract key entities from text"""
        entities = {
            'order_ids': [],
            'emails': [],
            'phone_numbers': [],
            'numbers': []
        }
        
        # Extract order IDs (patterns like ORD-123456, ORDER123456)
        order_pattern = r'(?:ORD|ORDER|ORDER#|ORDER_)[\s\-]?(\d+)'
        entities['order_ids'] = re.findall(order_pattern, text, re.IGNORECASE)
        
        # Extract emails
        email_pattern = r'\S+@\S+'
        entities['emails'] = re.findall(email_pattern, text)
        
        # Extract phone numbers
        phone_pattern = r'\b(?:\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\d{10})\b'
        entities['phone_numbers'] = re.findall(phone_pattern, text)
        
        # Extract numbers
        number_pattern = r'\b\d+(?:\.\d+)?\b'
        entities['numbers'] = re.findall(number_pattern, text)
        
        return entities
    
    @staticmethod
    def get_text_length_stats(text: str) -> dict:
        """Get text statistics"""
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        return {
            'word_count': len(words),
            'char_count': len(text),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'avg_word_length': sum(len(w) for w in words) / len(words) if words else 0
        }


class SentimentAnalyzer:
    """Sentiment analysis utilities"""
    
    @staticmethod
    def analyze_sentiment(text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text
        Returns: (sentiment_label, confidence_score)
        """
        from textblob import TextBlob
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  # -1 to 1
        
        # Map polarity to sentiment labels
        if polarity >= 0.5:
            return "very_positive", abs(polarity)
        elif polarity >= 0.1:
            return "positive", abs(polarity)
        elif polarity <= -0.5:
            return "very_negative", abs(polarity)
        elif polarity <= -0.1:
            return "negative", abs(polarity)
        else:
            return "neutral", 0.5
    
    @staticmethod
    def get_sentiment_keywords(text: str) -> dict:
        """Extract sentiment keywords from text"""
        positive_keywords = ['great', 'excellent', 'amazing', 'wonderful', 'good', 'satisfied', 'happy']
        negative_keywords = ['bad', 'terrible', 'awful', 'poor', 'disappointed', 'angry', 'frustrated']
        
        text_lower = text.lower()
        
        positive_found = [kw for kw in positive_keywords if kw in text_lower]
        negative_found = [kw for kw in negative_keywords if kw in text_lower]
        
        return {
            'positive': positive_found,
            'negative': negative_found
        }
