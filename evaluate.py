import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from app.preprocess import clean_text

df = pd.read_csv("data/sample_data.csv")
df['cleaned'] = df['text'].apply(clean_text)

X_train, X_test, y_train, y_test = train_test_split(
    df['cleaned'], df['category'], test_size=0.2, random_state=42, stratify=df['category']
)

vec = joblib.load("models/vectorizer.pkl")
model = joblib.load("models/model.pkl")

X_test_vec = vec.transform(X_test)
y_pred = model.predict(X_test_vec)
proba = model.predict_proba(X_test_vec)

accuracy = (y_pred == y_test).mean()
avg_confidence = proba.max(axis=1).mean()

print(f"Test accuracy: {accuracy:.4f}")
print(f"Average confidence on correct predictions: {avg_confidence:.4f}")