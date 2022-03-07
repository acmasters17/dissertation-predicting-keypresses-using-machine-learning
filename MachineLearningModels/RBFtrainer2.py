import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from Score import Score
from config import INPUT_CSV_FILENAME, RANDOM_STATE, FOLDS

# Load csv generated by DatasetGenerator directory
data = pd.read_csv('../DatasetGenerator/DataSets/' + INPUT_CSV_FILENAME)

# Separate features and label
X = data.iloc[:, :-1].values
# X = np.concatenate([X, X])
y = data.iloc[:, 20].values
# y = np.concatenate([y, y])

# Separate data into outer training and testing
sss = StratifiedShuffleSplit(n_splits=5, test_size=0.25, random_state=RANDOM_STATE)


# for i in range(1,51):
#     print("TRAINING:",i)
#     localf = 0
#     for train_index, test_index in sss.split(X, y):
#         X_train, X_test = X[train_index], X[test_index]
#         y_train, y_test = y[train_index], y[test_index]

#         model = KNeighborsClassifier(n_neighbors=i,weights="distance")
#         model.fit(X_train,y_train)


#         predicted = model.predict(X_test)

#         localf = localf + f1_score(y_test,predicted,average="weighted")

#     localf = localf / 5
#     print("Knn:",i," Local f1:",localf)



X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.20)
model = SVC(kernel="rbf")
scaler = StandardScaler()
X_scaled_train = scaler.fit_transform(X_train,y_train)
model.fit(X_scaled_train,y_train)
print(classification_report(y_test,model.predict(scaler.transform(X_test)),zero_division=0))