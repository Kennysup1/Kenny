from flask import Flask, render_template, request
import numpy as np
from sklearn.linear_model import LinearRegression

app = Flask(__name__)

# Train the model
sizes = np.array([[750], [800], [850], [900], [950], 
                  [1000], [1100], [1200], [1300], [1400]])
prices = np.array([150000, 160000, 170000, 180000, 190000, 
                   200000, 220000, 240000, 260000, 280000])

model = LinearRegression()
model.fit(sizes, prices)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    size = float(request.form['size'])
    prediction = model.predict([[size]])[0]
    return render_template('index.html', 
                         prediction=f"${prediction:,.0f}",
                         size=size)

if __name__ == '__main__':
    app.run(debug=True)