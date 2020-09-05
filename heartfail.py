#imports

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import pickle

#read csv file containing dataset
data = pd.read_csv(r"C:\Users\shashank\HeartFailData\heartfinal.csv")

#fill empty cells
data = data.fillna(0)

#exclude prediction result column
y = data["DEATH_EVENT"]
X = data.drop("DEATH_EVENT", axis=1)

#split the train and test data 
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2)


#using RandomForestClassifier
classifier = RandomForestClassifier(n_estimators = 50, criterion = 'entropy', random_state = 0)
#classifier = LogisticRegression(random_state=0, max_iter=1000)
#classifier = KNeighborsClassifier(n_neighbors=3)

classifier.fit(X_train, y_train)

pred = classifier.predict(X_test)

acc = accuracy_score(pred, y_test)

#get accuracy if required
#print(acc * 100)


#store trained model
pickle.dump(classifier, open('modelfinal.pickle', 'wb'))
