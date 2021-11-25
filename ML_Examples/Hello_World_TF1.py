
import tensorflow as tf
import numpy as np
from tensorflow import keras

model = tf.keras.Sequential([keras.layers.Dense(units=1, input_shape=[1])])

model.compile(optimizer='sgd', loss='mean_squared_error')

features = np.array ([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], dtype=float)
labels = np.array ([1.0, 1.50, 2.0, 2.5, 3.0, 3.5], dtype=float)

model.fit(features, labels, epochs=500)

print(model.predict([7.0]))