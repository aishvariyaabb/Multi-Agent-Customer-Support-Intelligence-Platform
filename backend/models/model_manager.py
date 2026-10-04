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

        self._train_default_models()

        # Load pre-trained models if they exist
        self._load_models()

    def _is_fitted(self, pipeline) -> bool:
        """Return True only if the pipeline has been fit."""
        try:
            clf = pipeline.named_steps.get('classifier')
            return hasattr(clf, 'classes_') and len(getattr(clf, 'classes_', [])) > 0
        except Exception:
            return False

    def _train_default_models(self):
        """Fit lightweight default classifiers so the app works immediately."""
        category_examples = [
            ("my order has not arrived yet", "delivery"),
            ("package was lost in transit", "delivery"),
            ("need refund for damaged item", "refund"),
            ("please refund my money", "refund"),
            ("payment failed twice", "payment"),
            ("charged incorrect amount", "payment"),
            ("product is broken", "product_issue"),
            ("item arrived damaged", "product_issue"),
            ("where is my order", "order_tracking"),
            ("track my shipment status", "order_tracking"),
            ("cannot log in to my account", "account"),
            ("reset my password", "account"),
            ("i need help with my subscription", "account"),
            ("billing question", "payment"),
            ("customer service issue", "other"),
        ]

        priority_examples = [
            ("can you tell me the status of my order", "low"),
            ("how do I change my password", "low"),
            ("my package is delayed", "medium"),
            ("refund not processed", "medium"),
            ("payment got charged twice", "high"),
            ("my account is locked and I cannot access order", "high"),
            ("this is urgent, my order never arrived and I need help now", "critical"),
            ("illegal charge and I want my money back immediately", "critical"),
        ]

        if not self._is_fitted(self.category_classifier.model):
            texts = [text for text, _ in category_examples]
            labels = [label for _, label in category_examples]
            self.category_classifier.train(texts, labels)

        if not self._is_fitted(self.priority_classifier.model):
            texts = [text for text, _ in priority_examples]
            labels = [label for _, label in priority_examples]
            self.priority_classifier.train(texts, labels)

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
