import logging
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from .preprocess import clean_text
from .model import load_artifacts

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Invoice Expense Classifier")

# ---------- Request/Response Models ----------
class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    category: str
    confidence: float
    top_keywords: List[str]

class BatchPredictRequest(BaseModel):
    texts: List[str]

class BatchPredictResponse(BaseModel):
    predictions: List[PredictResponse]

# ---------- Startup: load model once ----------
@app.on_event("startup")
def startup():
    load_artifacts()
    logger.info("Model and vectorizer loaded. API ready.")

# ---------- Helper: extract top keywords ----------
def get_top_keywords(model, vectorizer, cleaned_text: str, pred_idx: int) -> List[str]:
    try:
        # Try to get coefficients (works for LogisticRegression, also for CalibratedClassifierCV)
        if hasattr(model, "base_estimator") and hasattr(model.base_estimator, "coef_"):
            coef = model.base_estimator.coef_[pred_idx]
        elif hasattr(model, "coef_"):
            coef = model.coef_[pred_idx]
        else:
            raise AttributeError("No coefficients")
        feature_names = vectorizer.get_feature_names_out()
        top_indices = np.argsort(coef)[-3:][::-1]
        top_words = [feature_names[i] for i in top_indices if feature_names[i] in cleaned_text]
        if not top_words:
            top_words = [feature_names[i] for i in top_indices[:3]]
        return top_words[:3]
    except Exception as e:
        logger.warning(f"Keyword extraction failed: {e}")
        # Fallback: return any known words from the text
        vocab = set(vectorizer.get_feature_names_out())
        words = [w for w in cleaned_text.split() if w in vocab]
        return words[:3]

# ---------- Endpoint: Single prediction (POST) ----------
@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    model, vectorizer = load_artifacts()
    cleaned = clean_text(req.text)
    X = vectorizer.transform([cleaned])
    probs = model.predict_proba(X)[0]
    pred_idx = int(np.argmax(probs))
    category = model.classes_[pred_idx]
    confidence = float(probs[pred_idx])
    top_words = get_top_keywords(model, vectorizer, cleaned, pred_idx)
    
    logger.info(f"Predicted {category} with confidence {confidence:.2f} for: {req.text[:50]}")
    return PredictResponse(category=category, confidence=confidence, top_keywords=top_words)

# ---------- Endpoint: Batch prediction (POST) ----------
@app.post("/predict_batch", response_model=BatchPredictResponse)
def predict_batch(req: BatchPredictRequest):
    if not req.texts:
        raise HTTPException(status_code=400, detail="List of texts cannot be empty")
    
    model, vectorizer = load_artifacts()
    results = []
    for text in req.texts:
        if not text.strip():
            results.append(PredictResponse(category="", confidence=0.0, top_keywords=[]))
            continue
        cleaned = clean_text(text)
        X = vectorizer.transform([cleaned])
        probs = model.predict_proba(X)[0]
        pred_idx = int(np.argmax(probs))
        category = model.classes_[pred_idx]
        confidence = float(probs[pred_idx])
        top_words = get_top_keywords(model, vectorizer, cleaned, pred_idx)
        results.append(PredictResponse(category=category, confidence=confidence, top_keywords=top_words))
    
    return BatchPredictResponse(predictions=results)

# ---------- Health check ----------
@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": True}