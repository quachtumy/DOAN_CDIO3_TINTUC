import pandas as pd
import joblib

from processing.preprocessing.text_cleaning import clean_text
from underthesea import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score

def train():
    # Load data
    df = pd.read_csv('data/data.csv')

    # Preprocessing
    X = df['texts'].astype(str).apply(clean_text)
    X = X.apply(lambda x: word_tokenize(x, format='text'))
    
    y = df['category']

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # Label encoder
    encoder = LabelEncoder()
    y_train = encoder.fit_transform(y_train)
    y_test = encoder.transform(y_test)

    # TF-IDF
    vectorizer = TfidfVectorizer(
        max_features=20000,
        ngram_range=(1,2),
        min_df=2,
        max_df=0.9,
        sublinear_tf=True
    )
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    # Train model
    models = {
        'Logistic Regression': LogisticRegression(max_iter=2000, C=2.0, solver='liblinear', class_weight='balanced'),
        'Naive Bayes': MultinomialNB(alpha=0.5),
        'SVM': LinearSVC(C=2, class_weight='balanced', max_iter=5000)
    }

    accuracies = {}

    for name_model, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        accuracies[name_model] = acc
        print(f'{name_model}: {acc:.4f}')
    
    best_model_name = max(accuracies, key=accuracies.get)
    best_model = models[best_model_name]
    print('Best model: ', best_model_name)

    # Save models
    joblib.dump(best_model, 'models/model.pkl')
    joblib.dump(vectorizer, 'models/tfidf.pkl')
    joblib.dump(encoder, 'models/label_encoder.pkl')

    if __name__ == '__main__':
        train()

