# -*- coding: utf-8 -*-
"""IMDB Review Prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kdu0na-xlggXrJYyr9w_VvU6iHHsRjMU
"""

import pandas as pd
import numpy as np

url='https://raw.githubusercontent.com/devanshmarwaha26/IMDB-Dataset/master/IMDB%20Dataset.csv'
df=pd.read_csv(url).values

puncts=[ '?', '!', '.', ',', '"', '#', '$', '%', '\\', "'", '(', ')', '*', '+', '-', '/', ':', ';', '<', '=', '>', '@', '[', ']', '_', '`', '{', '|', '}', '~',  '“', '”', '’', '′', '…', '–', '‘',  '—', 'ʿ', 'ʻ', '−', '...',  '∖', '„',  '¸', '″',  '‑', '－', '＝', '（', '）', 'ː', 'Ο',]

X=df[:,0]
Y=df[:,1]

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()
Y=le.fit_transform(Y)

print(Y)

def lower(X):
  reviews=[]
  m=X.shape[0]
  for i in range(m):
    review=X[i].lower()
    review=review.replace('<br /><br />',' ')
    reviews.append(review)
  return np.array(reviews)

def punctuate(X):
  reviews=[]
  m=X.shape[0]
  for i in range(m):
    review=X[i]
    for ele in review:
      if ele in puncts:
        review=review.replace(ele,'')
    reviews.append(review)
  return np.array(reviews)

from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

import nltk
nltk.download('stopwords')

tokenize=RegexpTokenizer(r'\w+')
ss=SnowballStemmer('english')
en_stopwords=set(stopwords.words('english'))

def tokenizer(X):
  reviews=[]
  m=X.shape[0]
  for i in range(m):
    review=X[i]
    tokens=tokenize.tokenize(review)
    review=' '.join(tokens)
    reviews.append(review)
  return np.array(reviews)

def stemming(X):
  reviews=[]
  m=X.shape[0]
  for i in range(m):
    review=X[i]
    tokens=tokenize.tokenize(review)
    stem=[ss.stem(t) for t in tokens]
    stem=' '.join(stem)
    reviews.append(stem)
  return np.array(reviews)

def stopword_rm(X):
  reviews=[]
  m=X.shape[0]
  for i in range(m):
    review=X[i]
    tokens=tokenize.tokenize(review)
    new_tokens=[token for token in tokens if token not in en_stopwords]
    new_tokens=' '.join(new_tokens)
    reviews.append(new_tokens)
  return np.array(reviews)

X=lower(X)

def function(X):
  reviews=[]
  m=X.shape[0]
  for i in range(m):
    review=X[i]
    review=review.lower()
    review=review.replace('<br /><br />',' ')
    #for ele in review:
      #if ele in puncts:
        #review=review.replace(ele,'')
    tokens=tokenize.tokenize(review)
    stem=[ss.stem(t) for t in tokens]
    new_tokens=[token for token in tokens if token not in en_stopwords]
    new_tokens=' '.join(new_tokens)
    reviews.append(new_tokens)
  return np.array(reviews)

X1=function(X)

"""X2=tokenizer(X)
X2=stemming(X2)
X2=stopword_rm(X2)

X3=punctuate(X)
X3=stemming(X3)
X3=stopword_rm(X3)

X4=punctuate(X)
X4=tokenizer(X4)
X4=stopword_rm(X4)

X5=punctuate(X)
X5=tokenizer(X5)
X5=stemming(X5)

X6=stemming(X)

X7=tokenizer(X)
X7=stemming(X7)
"""

from sklearn.model_selection import train_test_split
x1_train,x1_test,y1_train,y1_test=train_test_split(X1,Y,test_size=0.4)
x1_val=x1_test[:10000]
y1_val=y1_test[:10000]
x1_test=x1_test[10000:]
y1_test=y1_test[10000:]

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer()
x1cv=cv.fit_transform(x1_train)

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf=TfidfVectorizer()
x1tf=tfidf.fit_transform(x1_train)

from sklearn.naive_bayes import MultinomialNB
mnb=MultinomialNB()

mnb.fit(x1cv,y1_train)

mnb.score(x1cv,y1_train)

x1cv_val=cv.transform(x1_val)
x1cv_test=cv.transform(x1_test)

mnb.score(x1cv_test,y1_test)

y_pred=mnb.predict(x1cv_test)

print(y1_test)

from sklearn.metrics import precision_recall_fscore_support
precision_recall_fscore_support(y1_test, y_pred, average='binary')

from sklearn.metrics import confusion_matrix
cnf=confusion_matrix(y1_test,y_pred)

print(cnf)

mnb1=MultinomialNB()

mnb1.fit(x1tf,y1_train)

mnb1.score(x1tf,y1_train)

x1tf_test=tfidf.transform(x1_test)

mnb1.score(x1tf_test,y1_test)

y_pred1=mnb1.predict(x1tf_test)

cnf1=confusion_matrix(y1_test,y_pred1)
print(cnf1)

precision_recall_fscore_support(y1_test, y_pred1, average='binary')

from sklearn.linear_model import LogisticRegression
params=[
        {'C':[0.01,0.03,0.1,0.3,1,3,10,30,100]}
]
from sklearn.model_selection import GridSearchCV

clf=LogisticRegression()
gs=GridSearchCV(estimator=clf,param_grid=params,scoring='f1',cv=5,n_jobs=-1)

x1tf_val=tfidf.transform(x1_val)

clf.fit(x1tf,y1_train)

clf.score(x1tf,y1_train)

gs.fit(x1tf_val,y1_val)

gs.best_estimator_

clf=LogisticRegression(C=3,max_iter=20)

x1tf

clf.fit(x1tf,y1_train)

clf.score(x1tf,y1_train)

clf.score(x1tf_val,y1_val)

clf.score(x1tf_test,y1_test)

clf.score(x1tf_val,y1_val)

y_pred2=clf.predict(x1tf_test)

cnf2=confusion_matrix(y1_test,y_pred2)
print(cnf2)

precision_recall_fscore_support(y1_test, y_pred2, average='binary')

from keras import models
from keras.layers import Dense

len(tfidf.vocabulary_)

#Define the model
model=models.Sequential()
model.add(Dense(16,activation='relu',input_shape=(82206,)))
model.add(Dense(16,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

#Compile the model
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

model.summary()

hist=model.fit(x1tf,y1_train,batch_size=512,epochs=3,validation_data=(x1tf_val,y1_val))

h=hist.history

import matplotlib.pyplot as plt

plt.plot(h['val_accuracy'],label='Validation Accuracy')
plt.plot(h['accuracy'],label='Training Accuracy')
plt.legend()
plt.style.use('seaborn')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.show()

model.evaluate(x1tf_test,y1_test)[1]

y_pred3=model.predict(x1tf_test)

y_pred3[y_pred3>=0.5]=1
y_pred3[y_pred3<0.5]=0

y_pred3=y_pred3.reshape((-1,))

y_pred3=y_pred3.astype('int32')

precision_recall_fscore_support(y1_test, y_pred3,average='binary')

cnf3=confusion_matrix(y1_test,y_pred3)
print(cnf3)

