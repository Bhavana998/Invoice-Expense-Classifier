import joblib
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model.pkl"
VEC_PATH = BASE_DIR / "models" / "vectorizer.pkl"

_model = None
_vectorizer = None

def load_artifacts():
    global _model, _vectorizer
    if _model is None:
        logger.info("Loading model and vectorizer...")
        _model = joblib.load(MODEL_PATH)
        _vectorizer = joblib.load(VEC_PATH)
        logger.info("Artifacts loaded successfully.")
    return _model, _vectorizer

def get_model():
    model, _ = load_artifacts()
    return model

def get_vectorizer():
    _, vec = load_artifacts()
    return vec