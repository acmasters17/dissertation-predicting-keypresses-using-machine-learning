import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
import sklearn.model_selection
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import cross_val_score

# Load csv generated by DatasetGenerator directory
data = pd.read_csv('../DatasetGenerator/DataSets/test.csv')

# Separate features and label
X = data.iloc[:,:-1].values 
y = data.iloc[:,20].values

sss = StratifiedShuffleSplit(n_splits=5, test_size=0.5, random_state=0)


SVM_rbf_scores = cross_val_score(SVC(kernel="rbf"), X, y, cv=sss, scoring="accuracy")
SVM_polynomial_scores = cross_val_score(SVC(kernel="poly"), X, y, cv=sss, scoring="accuracy")
SVM_linear_scores = cross_val_score(SVC(kernel="linear"), X, y, cv=sss, scoring="accuracy")

print(SVM_rbf_scores.mean())
print(SVM_polynomial_scores.mean())
print(SVM_linear_scores.mean())



# Train models
# SVM_rbf_model.fit(X_train, y_train)
# SVM_polynomial_model.fit(X_train, y_train)
# SVM_linear_model.fit(X_train, y_train)

# # Test Models
# SVM_rbf_prediction = SVM_rbf_model.predict(X_test)
# SVM_polynomial_prediction = SVM_polynomial_model.predict(X_test)
# SVM_linear_prediction = SVM_linear_model.predict(X_test)

# # Display some performance measures for models
# print("-------------------")
# print("RBF SVM")
# print("Accuracy for rbf SVM : " + str(accuracy_score(SVM_rbf_prediction, y_test)))
# print("Classification Report for rbf SVM")
# print(classification_report(SVM_rbf_prediction, y_test, zero_division=0))
# print("-------------------")

# print("-------------------")
# print("Polynomial SVM")
# print("Accuracy for polynomial SVM : " + str(accuracy_score(SVM_polynomial_prediction, y_test)))
# print("Classification Report for polynomial SVM")
# print(classification_report(SVM_polynomial_prediction, y_test, zero_division=0))
# print("-------------------")

# print("-------------------")
# print("Linear SVM")
# print("Accuracy for linear SVM : " + str(accuracy_score(SVM_linear_prediction, y_test)))
# print("Classification Report for linear SVM")
# print(classification_report(SVM_linear_prediction, y_test, zero_division=0))
# print("-------------------")




