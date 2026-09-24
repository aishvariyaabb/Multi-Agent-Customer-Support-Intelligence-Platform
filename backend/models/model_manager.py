"""
Trained models instance management
"""
from backend.models.classifiers import CategoryClassifier, PriorityClassifier, IntentExtractor
from backend.config import get_settings
import os


class ModelManager:
    """Manage all ML models"""
    
    def __init__(self):
        """Initialize all models"""
        settings = get_settings()
        self.models_path = settings.models_path
        
        self.category_classifier = CategoryClassifier()
        self.priority_classifier = PriorityClassifier()
        self.intent_extractor = IntentExtractor()
        
        # Load pre-trained models if they exist
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models from disk"""
        category_model_path = os.path.join(self.models_path, 'category_classifier.pkl')
        priority_model_path = os.path.join(self.models_path, 'priority_classifier.pkl')
        
        if os.path.exists(category_model_path):
            self.category_classifier.load(category_model_path)
        
        if os.path.exists(priority_model_path):
            self.priority_classifier.load(priority_model_path)
    
    def save_models(self):
        """Save all models to disk"""
        os.makedirs(self.models_path, exist_ok=True)
        self.category_classifier.save(os.path.join(self.models_path, 'category_classifier.pkl'))
        self.priority_classifier.save(os.path.join(self.models_path, 'priority_classifier.pkl'))


# Global model manager instance
_model_manager_instance = None


def get_model_manager() -> ModelManager:
    """Get global model manager instance"""
    global _model_manager_instance
    if _model_manager_instance is None:
        _model_manager_instance = ModelManager()
    return _model_manager_instance
