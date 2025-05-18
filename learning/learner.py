import keras

import numpy as np
import tensorflow.keras.backend as K

from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, Input, UpSampling2D, LSTM
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

from data.data_classes import Openings, Path

X = np.load("mazes.npy")
Y = np.load("paths.npy")

input_shape = X[0].shape
split = int(X.shape[0] * 0.9)
X_train, X_test = X[:split], X[split:]
Y_train, Y_test = Y[:split], Y[split:]

print(input_shape)

model = Sequential()
model.add(Input(shape=(100,)))
model.add(Dense(1000))
model.add(Dropout(0.2))
model.add(Dense(1000))
model.add(Dense(100, activation='linear'))

def within_0_1_accuracy(y_true, y_pred):
    return K.mean(K.less_equal(K.abs(y_true - y_pred), 0.1))
# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error', metrics=[within_0_1_accuracy])

# Train with NumPy arrays
model.fit(X_train, Y_train, epochs=10, batch_size=32, validation_data=(X_test, Y_test))

# Evaluate
loss, accuracy = model.evaluate(X_test, Y_test)
model.summary()
print("Training loss:", model.history.history['loss'])
print('Test loss:', loss)
print('Test accuracy:', accuracy)

while True:
    try:
        test = np.random.randint(len(X))
        print(Openings(10, np_array=X[test]))
        path = model(X[test:test+1], training=False)
        np_path = path[0].numpy()
        print(Path(10, np_path=np_path))
        print(Path(10, np_path=Y[test]))
        breakpoint()
    except:
        pass
