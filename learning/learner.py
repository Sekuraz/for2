import keras

import numpy as np

from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, Input, UpSampling2D
from keras.models import Sequential

from data.data_classes import Openings, Path

X = np.load("mazes.npy")
Y = np.load("paths.npy")

input_shape = X[0].shape + (1,)
split = int(X.shape[0] * 0.9)
X_train, X_test = X[:split], X[split:]
Y_train, Y_test = Y[:split], Y[split:]

print(input_shape)

model = Sequential()
model.add(Conv2D(64, (3, 3), activation='relu', padding='same', input_shape=input_shape))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))

model.add(MaxPooling2D((2, 2)))

model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))

model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))

# Output Layer
model.add(Conv2D(1, (1, 1), activation='sigmoid', padding='same'))


# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

# Train with NumPy arrays
model.fit(X_train, Y_train, epochs=3, batch_size=5000, validation_data=(X_test, Y_test))

# Evaluate
loss, accuracy = model.evaluate(X_test, Y_test)
model.summary()
print("Training loss:", model.history.history['loss'])
print('Test loss:', loss)
print('Test accuracy:', accuracy)

while True:
    test = np.random.randint(len(X))
    print(Openings(10, np_array=X[test]))
    path = model.predict(X)
    breakpoint()
    print(Path(10, np_path=path[test]))
    input()
