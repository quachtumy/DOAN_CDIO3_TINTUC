import joblib

from processing.preprocessing.text_cleaning import clean_text
from underthesea import word_tokenize

class NewsClassifier():
    def __init__(self):
        # Load model
        self.model = joblib.load('models/model.pkl')
        self.vectorizer = joblib.load('models/vectorizer.pkl')
        self.encoder = joblib.load('models/label_encoder.pkl')

    def preprocess(self, text):
        text = clean_text(text)
        text = word_tokenize(text, format='text')
        return text
    
    def predict(self, text):
        text = self.preprocess(text)
        text = self.vectorizer.transform([text])

        pred = self.model.predict(text)

        label = self.encoder.inverse_transform(pred)[0]

        return label
        

