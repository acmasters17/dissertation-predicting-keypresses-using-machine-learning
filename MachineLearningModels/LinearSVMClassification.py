import pandas as pd
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from Score import Score
plt.style.use('ggplot')

# Load csv generated by DatasetGenerator directory
data = pd.read_csv('../DatasetGenerator/DataSets/test.csv')

# Separate features and label
X = data.iloc[:, :-1].values
# X = np.concatenate([X, X])
y = data.iloc[:, 20].values
# y = np.concatenate([y, y])




# Defining config
randomState = 50
folds = 10

# Separate data into outer training and testing
X_outer_train, X_outer_test, y_outer_train, y_outer_test = train_test_split(X, y, test_size=0.25, random_state=randomState)


# Using stratified sampling on training set
sss = StratifiedShuffleSplit(n_splits=folds, test_size=0.33, random_state=randomState)

# choose C between 0 and 1
c_range = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
lin_svm_scores = []


# Hyper parameter tuning for box constraint C
for c in c_range:
    accuracy = 0
    precision = 0
    f1 = 0
    recall = 0
    # 10 fold cross validation
    for train_index, test_index in sss.split(X_outer_train, y_outer_train):
        # Create model
        model = SVC(kernel="linear",C=c)
        # Extract training and testing data
        X_inner_train, X_inner_test = X_outer_train[train_index], X_outer_train[test_index]
        y_inner_train, y_inner_test = y_outer_train[train_index], y_outer_train[test_index]
        # train the model and extract scores
        model.fit(X_inner_train, y_inner_train)
        prediction = model.predict(X_inner_test)
        accuracy += accuracy_score(y_inner_test, prediction)
        precision += precision_score(y_inner_test, prediction,
                                     zero_division=0, average="weighted")
        f1 += f1_score(y_inner_test, prediction, zero_division=0, average="weighted")
        recall += recall_score(y_inner_test, prediction, zero_division=0, average="weighted")
        

    # Computer average scores from cross fold
    accuracy = accuracy / folds
    precision = precision / folds
    f1 = f1 / folds
    recall = recall / folds

    # Add these two the array
    lin_svm_scores.append(Score(accuracy,precision,f1,recall))

# plot accuracy against c
plt.plot(c_range, list(map(lambda obj: obj.accuracy,lin_svm_scores)))
plt.xlabel('Value of C for Linear SVM')
plt.ylabel('Cross-Validated Accuracy')
plt.show()

# plot precision against c
plt.plot(c_range, list(map(lambda obj: obj.precision,lin_svm_scores)))
plt.xlabel('Value of C for Linear SVM')
plt.ylabel('Cross-Validated Precision')
plt.show()

# plot recall against c
plt.plot(c_range, list(map(lambda obj: obj.recall,lin_svm_scores)))
plt.xlabel('Value of C for Linear SVM')
plt.ylabel('Cross-Validated Recall')
plt.show()

# plot f1 against c
plt.plot(c_range, list(map(lambda obj: obj.f1,lin_svm_scores)))
plt.xlabel('Value of C for Linear SVM')
plt.ylabel('Cross-Validated F1 Score')
plt.show()

# Get best C based off best f score
fscores = list(map(lambda obj: obj.f1,lin_svm_scores))
bestC = c_range[fscores.index(max(fscores))]
print("Best C found - " + str(bestC))
print("Now trained on full dataset...")
# Train best model on whole dataset and show classification report
bestModel = SVC(kernel="linear", C=bestC)
bestModel.fit(X_outer_train,y_outer_train)
bestPrediction = bestModel.predict(X_outer_test)
print(classification_report(y_outer_test,bestPrediction,zero_division=0))
print(accuracy_score(y_outer_test,bestPrediction))
print(precision_score(y_outer_test,bestPrediction,zero_division=0,average="weighted"))
print(recall_score(y_outer_test,bestPrediction,zero_division=0,average="weighted"))
print(f1_score(y_outer_test,bestPrediction,zero_division=0,average="weighted"))