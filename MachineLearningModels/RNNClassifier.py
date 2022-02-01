import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from config import INPUT_CSV_FILENAME, RANDOM_STATE, FOLDS
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import tensorflow
from tensorflow.keras.layers import LSTM, Dense, Dropout

plt.style.use('ggplot')

# Load csv generated by DatasetGenerator directory
data = pd.read_csv('../DatasetGenerator/DataSets/' + INPUT_CSV_FILENAME)

# Separate features and label
X = data.iloc[:, :-1].values
# X = np.concatenate([X, X])
y = data.iloc[:, 20].values

# print(y)

categories = np.array(['Q', "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K", "L",
              "Z", "X", "C", "V", "B", "N", "M", ",", ";", "'", "Backspace", "FullStop", "Space"])


for i in range(0,len(y)):
    index = np.where(categories == y[i])[0]
    y[i] = index[0]




y = np.asarray(y).astype('float32')

# print(y)


# Separate data into outer training and testing
X_outer_train, X_outer_test, y_outer_train, y_outer_test = train_test_split(
    X, y, test_size=0.25, shuffle=True)

input_shape = (X_outer_train.shape[1],1)
model = tensorflow.keras.Sequential()
model.add(LSTM(128, input_shape=input_shape))
model.add(Dropout(0.2))
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(48, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(33, activation='softmax'))
model.summary()
model.compile(optimizer='adam',
              loss='SparseCategoricalCrossentropy', metrics=['acc'])
history = model.fit(X_outer_train, y_outer_train, epochs=50, batch_size=100,
                    validation_data=(X_outer_test, y_outer_test), shuffle=True)



