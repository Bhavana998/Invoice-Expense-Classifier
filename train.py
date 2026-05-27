import pandas as pd
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score
from app.preprocess import clean_text
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    Path("models").mkdir(exist_ok=True)
    
    # Load data
    df = pd.read_csv("data/sample_data.csv")
    logger.info(f"Loaded {len(df)} samples")
    df['cleaned'] = df['text'].apply(clean_text)
    
    # Vectorizer: rich n‑grams
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=30000,
        stop_words='english',
        sublinear_tf=True,
        min_df=2,
        max_df=0.85
    )
    X = vectorizer.fit_transform(df['cleaned'])
    y = df['category']
    
    # Base model
    base_model = LogisticRegression(
        C=1.0,
        class_weight='balanced',
        solver='liblinear',
        max_iter=2000,
        random_state=42
    )
    
    # Calibrated model (better confidence scores)
    calibrated_model = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)
    
    # Cross‑validation accuracy (on uncalibrated base model for speed)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_acc = cross_val_score(base_model, X, y, cv=cv, scoring='accuracy')
    logger.info(f"Cross‑validation accuracy: {cv_acc.mean():.4f} (+/- {cv_acc.std():.4f})")
    
    # Train calibrated model on all data
    calibrated_model.fit(X, y)
    
    # Save artifacts
    joblib.dump(vectorizer, "models/vectorizer.pkl")
    joblib.dump(calibrated_model, "models/model.pkl")
    logger.info("Model and vectorizer saved.")
    
    # Optional: show a few confidence examples
    logger.info("\nChecking confidence on training examples (should be high for clear cases):")
    sample_texts = [
        "AWS EC2 monthly hosting with data transfer",
        "DHL express courier for warehouse delivery",
        "Staples printer paper ream 500 sheets"
    ]
    for text in sample_texts:
        cleaned = clean_text(text)
        vec = vectorizer.transform([cleaned])
        proba = calibrated_model.predict_proba(vec)[0]
        pred = calibrated_model.classes_[np.argmax(proba)]
        conf = np.max(proba)
        logger.info(f"Text: {text[:50]}... → {pred} ({conf:.2f})")

if __name__ == "__main__":
    main()