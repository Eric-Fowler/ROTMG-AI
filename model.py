import tensorflow as tf
import keras
import numpy as np
import matplotlib.pyplot as plt

inputs = keras.Input(shape=(2,))
layer1 = keras.layers.Dense(4,activation='sigmoid')(inputs)


model = keras.Model(inputs=inputs,outputs=layer1)

model.build()
model.summary()