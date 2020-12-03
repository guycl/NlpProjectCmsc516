# Pandas
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn_crfsuite import CRF
from sklearn_crfsuite.metrics import flat_f1_score
from sklearn_crfsuite.metrics import flat_classification_report
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

# This is a class to get sentence. The each sentence will be list of tuples with its tag.
class sentence(object):
    def __init__(self, df):
        self.n_sent = 1
        self.df = df
        self.empty = False
        agg = lambda s : [(p, t) for  p, t in zip(s['Word'].values.tolist(),
                                                  s['Tag'].values.tolist())]
        self.grouped = self.df.groupby("Sentence #").apply(agg)
        self.sentences = [s for s in self.grouped]
        
    def get_text(self):
        try:
            s = self.grouped['Sentence: {}'.format(self.n_sent)]
            self.n_sent +=1
            return s
        except:
            return None

# Class to generate features
def word2features(sent, i):
    word = sent[i][0]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
    }
    if i > 0:
        word1 = sent[i-1][0]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
        })
    else:
        features['EOS'] = True

    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def sent2labels(sent):
    return [label for token, label in sent]

def sent2tokens(sent):
    return [token for token, label in sent]


# Read CSV
df = pd.read_csv('Development Data Annotated\combined.csv', encoding = "ISO-8859-1")
df = df.drop(['Line #'], axis = 1)
#print(df.head(10))
#print(df.describe())

# Fill in NaN values of sentence
df = df.fillna(method = 'ffill')

# Combine sentences based on sentence number
getter = sentence(df)
sentences = [" ".join([s[0] for s in sent]) for sent in getter.sentences]

sentences = getter.sentences

X = [sent2features(s) for s in sentences]
y = [sent2labels(s) for s in sentences]

# 80%/20% train/test split validation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

crf = CRF(algorithm = 'lbfgs',
         c1 = 0.1,
         c2 = 0.1,
         max_iterations = 100,
         all_possible_transitions = False)
crf.fit(X_train, y_train)

y_pred = crf.predict(X_test)

f1_score = flat_f1_score(y_test, y_pred, average = 'weighted')
print(f1_score)

report = flat_classification_report(y_test, y_pred)
print(report)


# 10-fold cross validation
print("Cross validation")

cv = KFold(n_splits=10, random_state=1, shuffle=True)
scores = cross_val_score(crf, X, y, cv=cv, n_jobs=-1)
print("Accuracy: %0.2f (%0.2f)" % (scores.mean(), scores.std()))
