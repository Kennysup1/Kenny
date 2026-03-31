from flask import Flask, render_template, request, jsonify
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
import nltk

nltk.download('punkt')
nltk.download('punkt_tab')

app = Flask(__name__, template_folder='summarizer_templates')

def summarize_text(text, sentences=3, method='lsa'):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    
    if method == 'lsa':
        summarizer = LsaSummarizer()
    elif method == 'lexrank':
        summarizer = LexRankSummarizer()
    else:
        summarizer = LuhnSummarizer()
    
    summary = summarizer(parser.document, sentences)
    return ' '.join([str(sentence) for sentence in summary])

@app.route('/')
def home():
    return render_template('summarizer.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.form['text']
    sentences = int(request.form.get('sentences', 3))
    method = request.form.get('method', 'lsa')
    
    if len(text.split()) < 30:
        return jsonify({'error': 'Text is too short! Please enter at least 30 words.'})
    
    summary = summarize_text(text, sentences, method)
    
    original_words = len(text.split())
    summary_words = len(summary.split())
    reduction = round((1 - summary_words/original_words) * 100)
    
    return jsonify({
        'summary': summary,
        'original_words': original_words,
        'summary_words': summary_words,
        'reduction': reduction
    })

if __name__ == '__main__':
    app.run(debug=True, port=5005)