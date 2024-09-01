import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn import metrics
import joblib


# Sample dataset for demonstration (use a real dataset)
# Load the dataset
df = pd.read_csv('/home/mujtaba/Desktop/comments/labeled_data.csv')

# Preprocess the data: Use the relevant columns
df = df[['tweet', 'class']]
df.columns = ['text', 'label']  # Renaming columns to match our code
df['label'] = df['label'].map({0: 1, 1: 0, 2: 0})  # Mapping: 0 = hate speech, 1 = offensive, 2 = neither

df = pd.DataFrame(df)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Create a pipeline that vectorizes the data then applies Naive Bayes
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(metrics.classification_report(y_test, y_pred))

# The model can now be used to predict whether a comment is hate speech

joblib.dump(model, 'hate_speech_model.pkl')
