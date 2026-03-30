from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from sklearn.linear_model import LinearRegression
from textblob import TextBlob

app = FastAPI(title="Kenny AI API", version="1.0.0")

# Train house price model
np.random.seed(42)
n = 200
sizes = np.random.randint(500, 3000, n)
bedrooms = np.random.randint(1, 6, n)
bathrooms = np.random.randint(1, 4, n)
age = np.random.randint(1, 50, n)
prices = (sizes * 150) + (bedrooms * 10000) + (bathrooms * 8000) - (age * 500) + np.random.randint(-10000, 10000, n)

X = np.column_stack([sizes, bedrooms, bathrooms, age])
house_model = LinearRegression()
house_model.fit(X, prices)

# Input models
class HouseInput(BaseModel):
    size: float
    bedrooms: int
    bathrooms: int
    age: int

class SentimentInput(BaseModel):
    text: str

class ChurnInput(BaseModel):
    age: int
    monthly_charges: float
    tenure_months: int
    num_products: int

# Routes
@app.get("/")
def home():
    return {
        "message": "Welcome to Kenny AI API!",
        "version": "1.0.0",
        "endpoints": [
            "/predict/house-price",
            "/predict/sentiment",
            "/predict/churn",
            "/health"
        ]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "models": ["house_price", "sentiment", "churn"]}

@app.post("/predict/house-price")
def predict_house_price(data: HouseInput):
    features = np.array([[data.size, data.bedrooms, data.bathrooms, data.age]])
    prediction = house_model.predict(features)[0]
    return {
        "input": data.dict(),
        "predicted_price": f"${prediction:,.0f}",
        "price_value": round(prediction, 2)
    }

@app.post("/predict/sentiment")
def predict_sentiment(data: SentimentInput):
    blob = TextBlob(data.text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    return {
        "text": data.text,
        "polarity": round(polarity, 2),
        "sentiment": sentiment
    }

@app.post("/predict/churn")
def predict_churn(data: ChurnInput):
    from sklearn.ensemble import RandomForestClassifier
    import pandas as pd

    np.random.seed(42)
    churn_data = {
        'age': np.random.randint(18, 65, 200),
        'monthly_charges': np.random.uniform(20, 100, 200),
        'tenure_months': np.random.randint(1, 72, 200),
        'num_products': np.random.randint(1, 5, 200),
        'churned': np.random.randint(0, 2, 200)
    }
    df = pd.DataFrame(churn_data)
    X = df[['age', 'monthly_charges', 'tenure_months', 'num_products']]
    y = df['churned']
    churn_model = RandomForestClassifier(n_estimators=100, random_state=42)
    churn_model.fit(X, y)

    features = np.array([[data.age, data.monthly_charges, data.tenure_months, data.num_products]])
    prediction = churn_model.predict(features)[0]
    probability = churn_model.predict_proba(features)[0][1]

    return {
        "input": data.dict(),
        "will_churn": bool(prediction),
        "churn_probability": f"{probability * 100:.1f}%",
        "recommendation": "High risk customer!" if prediction else "Customer likely to stay"
    }