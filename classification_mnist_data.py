# -*- coding: utf-8 -*-
"""classification Mnist data.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YmjiWyevbyj56y5Bt8MVeYrMW1WCf1il
"""

print(X_train.shape, y_train.shape)
print(X_test.shape, y_test.shape)

X_train[8]

y_train [8]

# import tools
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras import utils
from sklearn.metrics import confusion_matrix
import seaborn as sns

# import data
from keras.datasets import mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()

# first, let‘s generate a random number with numpy random, so everytime we get a different image
random_nr = np.random.randint(0, 60000)

# now, let‘s use imshow() to visualize the random number from our train dataset
plt.imshow(X_train[random_nr], cmap="gray");

random_nr

# Let‘s visualize one example per each digit using a for loop and matplotlib subplot
num_classes = 10

# Create a subplot
fig, ax = plt.subplots(1, num_classes, figsize=(20,20)) # 1 row, 10 columns (num_classes)

# Loop through 10 classes from train dataset and add labels from test dataset
for i in range(num_classes):
  sample = X_train[y_train == i][0]
  ax[i].imshow(sample, cmap="gray")
  ax[i].set_title(f"Label:{i}")

sample0 = X_train[y_train == 0]

sample0.shape

sample0[1200]

y_train[2098]

# encode labels
# the labels are integer numbers. we need to encod them using one hot encoding method-----> we will get labels in binary
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)
y_train.shape
y_test.shape
y_train[0]
y_test[0]

# Data Preprocessing
# normalize the images ------ the pixel value range 0-255, convert it to 0-1
X_train = X_train/255.0
X_test = X_test/255.0

# reshape data
X_train.shape

# flatten the train  and test input data. the DL model is just a dens NN or Fully connected NN. the dimension of Dens layer is just 1D can not process 2D data
X_train = X_train.reshape(X_train.shape[0], -1)
X_test = X_test.reshape(X_test.shape[0], -1)

X_train.shape

#Building the model
# Dens NN . first layer has 128 nodes and activation function is ReLU. Second Layer is Dens layer has  128 nodes and activation function is ReLU. last layer is a classification layer has 10 classes (activation function is softmax)
# Drop out is a technique used in NN to drop randamly number of nodes in the training process to avoid overfitting
model = Sequential()

model.add(Dense(units=128, input_shape=(784, ), activation="relu"))
model.add(Dense(units=128, activation="relu"))
model.add(Dropout(0.25))
model.add(Dense(units=10, activation="softmax"))

model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
model.summary()

# lets train the model: Batch size 512, # epochs 20
history = model.fit(X_train, y_train , epochs=20, batch_size=512,
                     validation_data=(X_test, y_test))

#plot the training and validation accuracy and loss at each epoch
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'y', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Train using Kfold cross validation
from sklearn.model_selection import KFold
def create_model():
  model = Sequential()
  model.add(Dense(units=128, input_shape=(784, ), activation="relu"))
  model.add(Dense(units=128, activation="relu"))
  model.add(Dropout(0.25))
  model.add(Dense(units=10, activation="softmax"))
  model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
  return model

# K-Fold Cross-Validation
kf = KFold(n_splits=5)
fold_no = 1
accuracies = []




for train_index, val_index in kf.split(X_train):
    print(f'Training fold {fold_no}...')

    X_train2, X_val2 = X_train[train_index], X_train[val_index]
    y_train2, y_val2 = y_train[train_index], y_train[val_index]

    model = create_model()
    model.fit(X_train2, y_train2, epochs=20, batch_size=512, verbose=0)

    # Evaluate the model
    val_loss, val_accuracy = model.evaluate(X_val2, y_val2, verbose=0)
    accuracies.append(val_accuracy)
    print(f'Fold {fold_no} - Validation Accuracy: {val_accuracy:.4f}')

    model.save(f'model_fold_{fold_no}.h5')

    fold_no += 1

# Print the average accuracy across folds
print(f'Average Accuracy: {np.mean(accuracies):.4f}')

test_accuracies = []

for fold in range(1, 6):
    model = keras.models.load_model(f'model_fold_{fold}.h5')
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    test_accuracies.append(test_accuracy)
    print(f'Test Accuracy for Fold {fold}: {test_accuracy:.4f}')

f'model_fold_{fold}.h5'