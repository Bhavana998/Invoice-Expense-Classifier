import pandas as pd
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report
from app.preprocess import clean_text
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    Path("models").mkdir(exist_ok=True)
    
    df = pd.read_csv("data/sample_data.csv")
    logger.info(f"Loaded {len(df)} samples")
    df['cleaned'] = df['text'].apply(clean_text)
    
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=20000,
        stop_words='english',
        sublinear_tf=True,
        min_df=2,
        max_df=0.85
    )
    X = vectorizer.fit_transform(df['cleaned'])
    y = df['category']
    
    # CHANGE: solver='lbfgs' (supports multiclass)
    base_model = LogisticRegression(C=1.0, class_weight='balanced', solver='lbfgs', max_iter=2000, random_state=42)
    
    # Calibrated model for better confidence
    calibrated_model = CalibratedClassifierCV(base_model, method='sigmoid', cv=5)
    calibrated_model.fit(X, y)
    
    # Optional cross‑validation (using base model for speed)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    try:
        cv_scores = cross_val_score(base_model, X, y, cv=cv, scoring='accuracy')
        logger.info(f"Cross-validation accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    except Exception as e:
        logger.warning(f"CV failed: {e}")
    
    # Save artifacts
    joblib.dump(vectorizer, "models/vectorizer.pkl")
    joblib.dump(calibrated_model, "models/model.pkl")
    logger.info("Model and vectorizer saved.")
    
    # Quick test on short inputs
    test_texts = ["AWS monthly cloud hosting bill", "DHL courier charges", "Staples printer paper"]
    for text in test_texts:
        cleaned = clean_text(text)
        X_test = vectorizer.transform([cleaned])
        proba = calibrated_model.predict_proba(X_test)[0]
        pred = calibrated_model.classes_[np.argmax(proba)]
        conf = np.max(proba)
        logger.info(f"'{text}' → {pred} ({conf:.3f})")

if __name__ == "__main__":
    main()