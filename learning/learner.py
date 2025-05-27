import numpy as np

from data.data_classes import Openings, Path

from tensorflow.keras.layers import BatchNormalization, Add, Conv1D, Conv2D, MaxPooling2D, Dense, Dropout, Flatten, Input, UpSampling2D, LSTM, TimeDistributed
from tensorflow.keras.models import Sequential, Model

X = np.load("mazes.npy").reshape(-1, 10, 10)
Y = np.load("paths.npy")

print(Openings(10, np_array=X[0].reshape(100,)))
print(Path(10, np_path=Y[0]))



x = Input(shape=(100,1))
conv1 = Conv2D(128, 5, padding='same', activation='relu')(x)
conv2 = Conv2D(128, 5, padding='same', activation='relu')(conv1)
flat = Flatten()(conv2)
action = Dense(4, activation='sigmoid')(flat) # model 1
critic = Dense(1, activation='sigmoid')(flat) # model 2

model1 = Model(inputs=x, outputs=action)

model.compile(optimizer='adam', loss='ppo', metrics='accuracy')


# Train with NumPy arrays
model.fit(X_train, Y_train, epochs=50, batch_size=1, validation_data=(X_test, Y_test))
