import keras

import numpy as np
import tensorflow.keras.backend as K

from tensorflow.keras.callbacks import EarlyStopping

from tensorflow.keras.layers import BatchNormalization, Add, Conv1D, Conv2D, MaxPooling2D, Dense, Dropout, Flatten, Input, UpSampling2D, LSTM, TimeDistributed
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.losses import Huber

from tensorflow.keras.optimizers import Adam, Nadam
from tensorflow.python.util.numpy_compat import np_array

from data.data_classes import Openings, Path

X = np.load("observations.npy")
Y = np.load("actions.npy")

input_shape = X[0].shape
split = int(X.shape[0] * 0.9)
X_train, X_test = X[:split], X[split:]
Y_train, Y_test = Y[:split], Y[split:]

print(input_shape)

########## Conv1D
model = Sequential()
model.add(Input(shape=(102,)))
model.add(Conv1D(64, 5, padding='same', activation='relu'))
model.add(Conv1D(64, 5, padding='same', activation='relu'))
model.add(Dropout(0.1))
model.add(Conv1D(64, 5, padding='same', activation='relu'))
model.add()
######### LSTM
# model.add(LSTM(128, return_sequences=True, dropout=0.2, recurrent_dropout=0.2))
# model.add(TimeDistributed(Dense(1, activation='linear')))
# model.add(Flatten())

# ############Recurring
#
# input_layer = Input(shape=(100, 1))  # Input shape: (batch_size, 100, 1)
#
# # First block
# x = Conv1D(128, 5, padding='same', activation='relu')(input_layer)
# x = Conv1D(128, 5, padding='same', activation='relu')(x)
#
# # Residual connection from input to after 2nd Conv
# residual = Conv1D(128, 1, padding='same')(input_layer)  # match channel dimensions
# x = Add()([x, residual])
#
# x = Dropout(0.3)(x)
#
# # Second block
# x = Conv1D(64, 5, padding='same', activation='relu')(x)
# x = Conv1D(1, 5, padding='same', activation='linear')(x)
#
# # Optional residual to preserve raw input influence
# output = Add()([x, Conv1D(1, 1, padding='same')(input_layer)])
#
# # Flatten to match label shape: (batch_size, 100)
# output = Flatten()(output)
#
# # Build and compile
# model = Model(inputs=input_layer, outputs=output)

def within_accuracy(y_true, y_pred):
    return K.mean(K.less_equal(K.abs(y_true - y_pred), 0.1))

# Compile the model
model.compile(optimizer=Nadam(learning_rate=0.001), loss=Huber(), metrics=[within_accuracy])

early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Train with NumPy arrays
model.fit(X_train, Y_train, epochs=50, batch_size=32, validation_data=(X_test, Y_test), callbacks=[early_stopping])

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
        path = model.predict(X[test:test+1])
        np_path = path[0]
        print(Path(10, np_path=np_path))
        print(Path(10, np_path=Y[test]))
        breakpoint()
    except Exception as e:
        print(e)
        input()
        pass
