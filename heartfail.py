import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import pickle
data = pd.read_csv("heartfailure.csv")

y = data["DEATH_EVENT"]

X = data.drop("DEATH_EVENT", axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.25)

classifier = RandomForestClassifier(n_estimators = 100, criterion = 'entropy', random_state = 0)
#classifier = LogisticRegression(random_state=0, max_iter=1000000)
#classifier = KNeighborsClassifier(n_neighbors=100)

classifier.fit(X_train, y_train)

pred = classifier.predict(X_test)

acc = accuracy_score(pred, y_test)

print(acc * 100)
pickle.dump(classifier, open('modelfinal.pickle', 'wb'))        

