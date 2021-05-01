import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import nltk
from nltk.corpus import stopwords
import re
import numpy as np
from bs4 import BeautifulSoup
from sklearn.svm import LinearSVC
import csv

data=pd.read_csv('IMDB Dataset.csv')
dat=data.copy()
final=dat.dropna()
nltk.download('wordnet')

x=final.drop(['sentiment'],axis=1)
y=final["sentiment"]
for i in y.index:
  if y[i]=="positive":
    y[i]=1
  elif y[i]=="negative":
    y[i]=0

review = dat['review'].loc[1]
soup = BeautifulSoup(review, "html.parser")
review = soup.get_text()

from sklearn.model_selection import train_test_split

dataset_train, dataset_test, train_data_label, test_data_label = train_test_split(dat['review'], dat['sentiment'], test_size=0.25, random_state=42)

train_data_label = (train_data_label.replace({'positive': 1, 'negative': 0})).values
test_data_label  = (test_data_label.replace({'positive': 1, 'negative': 0})).values

#nltk.download('stopwords')
corpus_train = []
corpus_test  = []
with open('finalReview.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["review", "sentiment"])
    for i in range(dataset_train.shape[0]):
        soup = BeautifulSoup(dataset_train.iloc[i], "html.parser")
        review = soup.get_text()
        review = re.sub('\[[^]]*\]', ' ', review)
        review = re.sub('[^a-zA-Z]', ' ', review)
        review = review.lower()
        review = review.split()
        review = [word for word in review if not word in set(stopwords.words('english'))]
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review]
        review = ' '.join(review)
        writer.writerow([review, train_data_label[i]])
        corpus_train.append(review)
      
    for j in range(dataset_test.shape[0]):
        soup = BeautifulSoup(dataset_test.iloc[j], "html.parser")
        review = soup.get_text()
        review = re.sub('\[[^]]*\]', ' ', review)
        review = re.sub('[^a-zA-Z]', ' ', review)
        review = review.lower()
        review = review.split()
        review = [word for word in review if not word in set(stopwords.words('english'))]
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review]
        review = ' '.join(review)
        writer.writerow([review, test_data_label[j]])
        corpus_test.append(review)

tfidf_vec = TfidfVectorizer(ngram_range=(1, 3))

tfidf_vec_train = tfidf_vec.fit_transform(corpus_train)
tfidf_vec_test = tfidf_vec.transform(corpus_test)

linear_svc = LinearSVC(C=0.5, random_state=42)
linear_svc.fit(tfidf_vec_train, train_data_label)

predict = linear_svc.predict(tfidf_vec_test)

check =pd.read_csv('dataset.csv')

Test_Data = check['Review']

Checker_Data = tfidf_vec.transform(Test_Data)
predict_test = linear_svc.predict(Checker_Data)

filename = 'final_model.sav'
joblib.dump(linear_svc,filename)

#model.predict([['best movie']])

# predict_test = pd.DataFrame(predict_test,  columns=['Sentiment'])

# new_dataframe = pd.concat([check, predict_test], axis=1)

# new_dataframe.to_csv('Result1.csv')

# Movie_name = new_dataframe.Movie.unique()
# Movie_name = Movie_name[:250]

# count = 1
# index = 0
# overall = []
# while count<= 250:
#   temp_count = 0
#   review = 0
#   while temp_count < 3:
#     review += new_dataframe.Sentiment[index]
#     index += 1
#     temp_count += 1
#   if review/4 <0.5:
#     overall.append("Negative")
#   elif review/4 >= 0.5:
#     overall.append("Positive")
#   count += 1

# Overall_Rating = pd.concat([pd.DataFrame(Movie_name), pd.DataFrame(overall)], axis = 1)
# Overall_Rating.columns = ['Movie Name', 'Overall Review']

# Overall_Rating.to_csv('Result2.csv')

