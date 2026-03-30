from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from textblob import TextBlob
from datetime import datetime

app = Flask(__name__, template_folder='sentiment_templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sentiments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    sentiment = db.Column(db.String(20), nullable=False)
    polarity = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    reviews = Review.query.order_by(Review.date.desc()).all()
    positive = Review.query.filter_by(sentiment='Positive').count()
    negative = Review.query.filter_by(sentiment='Negative').count()
    neutral = Review.query.filter_by(sentiment='Neutral').count()
    return render_template('sentiment.html',
                         reviews=reviews,
                         positive=positive,
                         negative=negative,
                         neutral=neutral)

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        sentiment = 'Positive'
    elif polarity < 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    review = Review(text=text, sentiment=sentiment, polarity=round(polarity, 2))
    db.session.add(review)
    db.session.commit()

    return jsonify({
        'text': text,
        'sentiment': sentiment,
        'polarity': round(polarity, 2)
    })

@app.route('/clear', methods=['POST'])
def clear():
    Review.query.delete()
    db.session.commit()
    return jsonify({'message': 'cleared'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)