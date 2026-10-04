"""
Train classifiers using the full support tickets CSV and save models.
"""
import os
import sys
from pathlib import Path
import pandas as pd

# Ensure project root is on path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.models.classifiers import CategoryClassifier, PriorityClassifier
from backend.models.model_manager import ModelManager
from backend.config import get_settings


def detect_columns(df: pd.DataFrame):
    subject_col = None
    description_col = None
    category_col = None
    priority_col = None

    for col in df.columns:
        col_lower = col.lower()
        if 'subject' in col_lower or 'issue' in col_lower or 'title' in col_lower:
            subject_col = col
        if 'description' in col_lower or 'details' in col_lower or 'message' in col_lower or 'ticket_text' in col_lower:
            description_col = col
        if 'category' in col_lower or 'ticket_category' in col_lower:
            category_col = col
        if 'priority' in col_lower:
            priority_col = col

    return subject_col, description_col, category_col, priority_col


def normalize_category(cat: str) -> str:
    if not isinstance(cat, str):
        return 'other'
    c = cat.lower()
    if 'refund' in c:
        return 'refund'
    if 'payment' in c or 'emi' in c:
        return 'payment'
    if 'delivery' in c or 'deliv' in c:
        return 'delivery'
    if 'product' in c or 'issue' in c:
        return 'product_issue'
    if 'order' in c or 'tracking' in c:
        return 'order_tracking'
    if 'account' in c or 'login' in c:
        return 'account'
    return 'other'


def normalize_priority(p: str) -> str:
    if not isinstance(p, str):
        return 'medium'
    s = p.lower()
    if 'critical' in s:
        return 'critical'
    if 'high' in s:
        return 'high'
    if 'low' in s:
        return 'low'
    return 'medium'


def main():
    print("🚧 Training script starting...")
    project = project_root
    # locate tickets CSV
    tickets_file = None
    for pattern in ['*ticket*.csv', '*support*.csv', '*10k*.csv']:
        matches = list(project.glob(pattern))
        if matches:
            tickets_file = str(matches[0])
            break

    if not tickets_file:
        print("❌ No tickets CSV found in project root")
        return

    print(f"📥 Loading tickets from: {tickets_file}")
    df = pd.read_csv(tickets_file)
    print(f"   Found {len(df)} rows")

    subject_col, desc_col, cat_col, prio_col = detect_columns(df)
    print(f"   Detected columns: subject={subject_col}, description={desc_col}, category={cat_col}, priority={prio_col}")

    texts = []
    cat_labels = []
    prio_labels = []

    for idx, row in df.iterrows():
        text = None
        if desc_col and pd.notna(row.get(desc_col)):
            text = str(row.get(desc_col)).strip()
        elif subject_col and pd.notna(row.get(subject_col)):
            text = str(row.get(subject_col)).strip()

        if not text:
            continue

        texts.append(text)

        cat_raw = row.get(cat_col) if cat_col else None
        prio_raw = row.get(prio_col) if prio_col else None

        cat_labels.append(normalize_category(cat_raw))
        prio_labels.append(normalize_priority(prio_raw))

    print(f"   Prepared {len(texts)} training examples")

    if len(texts) < 10:
        print("❗ Not enough data to train (need >=10). Aborting.")
        return

    # Train category classifier
    print("\n🔧 Training CategoryClassifier...")
    cat_clf = CategoryClassifier()
    cat_clf.train(texts, cat_labels)
    models_dir = get_settings().models_path
    os.makedirs(models_dir, exist_ok=True)
    cat_path = os.path.join(models_dir, 'category_classifier.pkl')
    cat_clf.save(cat_path)
    print(f"   ✅ Saved CategoryClassifier to {cat_path}")

    # Train priority classifier
    print("\n🔧 Training PriorityClassifier...")
    prio_clf = PriorityClassifier()
    prio_clf.train(texts, prio_labels)
    prio_path = os.path.join(models_dir, 'priority_classifier.pkl')
    prio_clf.save(prio_path)
    print(f"   ✅ Saved PriorityClassifier to {prio_path}")

    # Optionally create a ModelManager and save
    try:
        mm = ModelManager()
        mm.save_models()
        print("\n💾 ModelManager saved all models")
    except Exception:
        pass

    print("\n✅ Training complete.")


if __name__ == '__main__':
    main()
