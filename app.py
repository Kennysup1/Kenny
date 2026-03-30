from flask import Flask, render_template, request, jsonify
import numpy as np
from sklearn.linear_model import LinearRegression
import json

app = Flask(__name__)

# Train model with more features
# Features: size, bedrooms, bathrooms, age
np.random.seed(42)
n = 200
sizes = np.random.randint(500, 3000, n)
bedrooms = np.random.randint(1, 6, n)
bathrooms = np.random.randint(1, 4, n)
age = np.random.randint(1, 50, n)
prices = (sizes * 150) + (bedrooms * 10000) + (bathrooms * 8000) - (age * 500) + np.random.randint(-10000, 10000, n)

X = np.column_stack([sizes, bedrooms, bathrooms, age])
model = LinearRegression()
model.fit(X, prices)

history = []

@app.route('/')
def home():
    return render_template('index.html', history=history)

@app.route('/predict', methods=['POST'])
def predict():
    size = float(request.form['size'])
    bedrooms = float(request.form['bedrooms'])
    bathrooms = float(request.form['bathrooms'])
    age = float(request.form['age'])

    features = np.array([[size, bedrooms, bathrooms, age]])
    prediction = model.predict(features)[0]

    result = {
        'size': size,
        'bedrooms': int(bedrooms),
        'bathrooms': int(bathrooms),
        'age': int(age),
        'price': f"${prediction:,.0f}"
    }
    history.insert(0, result)

    return render_template('index.html',
                         prediction=f"${prediction:,.0f}",
                         history=history[:5])

if __name__ == '__main__':
    app.run(debug=True)