import pickle
import pandas as pd
from nltk.corpus.reader import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import classification_report


url = 'Champions_League_data2.txt'
data = pd.read_csv(url, index_col=False, sep=": ", names=["question", "group"])
df = pd.DataFrame(data)

stopwords = set(stopwords.words('english'))
vectorizer = TfidfVectorizer(stop_words=list(stopwords))

X = df.question
Y = df.group

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.25, train_size=0.75, random_state=1234,
                                                    shuffle='True')

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

naive_bayes = MultinomialNB()
naive_bayes.fit(X_train, y_train)

pred = naive_bayes.predict(X_test)
print(confusion_matrix(y_test, pred))

print(classification_report(y_test, pred))

print('accuracy score: ', accuracy_score(y_test, pred))

with open('classifier', 'wb') as picklefile:
    pickle.dump(naive_bayes, picklefile)

vec_file = 'vectorizer.pickle'
pickle.dump(vectorizer, open(vec_file, 'wb'))
