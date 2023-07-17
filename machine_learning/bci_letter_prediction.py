import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense
import numpy as np
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import pandas as pd
import json
from datetime import datetime

def train_model():
    # Keystroke data
    keystroke_df = pd.read_csv('keystroke_data.csv', names=['key', 'time'])
    keystroke_data = [{'key': row['key'], 'time': datetime.strptime(
        row['time'], "%Y-%m-%d %H:%M:%S.%f"
    )} for index, row in keystroke_df.iterrows()]

    # Brain data
    brain_df = pd.read_csv('brain_data.csv', names=['data', 'time'])
    brain_data = [{'data': json.loads(row['data']), 'time': datetime.strptime(
        row['time'], "%Y-%m-%d %H:%M:%S.%f")} for index, row in brain_df.iterrows()]

    print(keystroke_data)
    print(brain_data)

    # splitting the data into train and test
    keystrokes_train, keystrokes_test, brain_train, brain_test = train_test_split(keystroke_df, brain_df, test_size=0.2,
                                                                                  random_state=42)

    # scaling the data
    scaler = StandardScaler()

    keystrokes_train = scaler.fit_transform(keystrokes_train)
    keystrokes_test = scaler.transform(keystrokes_test)

    brain_train = scaler.fit_transform(brain_train)
    brain_test = scaler.transform(brain_test)

    # # initialize the model
    # model = Sequential()
    #
    # # add input layer with 32 units and a 'relu' activation function
    # model.add(Dense(32, input_dim=keystrokes_train.shape[1], activation='relu'))
    #
    # # add a hidden layer with 16 units and a 'relu' activation function
    # model.add(Dense(16, activation='relu'))
    #
    # # add output layer with number of units equal to the number of features in brain_data
    # # use linear activation function for regression problem, for classification problem use 'sigmoid' or 'softmax'
    # model.add(Dense(brain_train.shape[1], activation='linear'))
    #
    # # compile the model
    # model.compile(loss='mse', optimizer=Adam(), metrics=['mae'])  # mean squared error loss for regression problem,
    # for classification problem use 'binary_crossentropy' or 'categorical_crossentropy'
    #
    # # train the model
    # history = model.fit(keystrokes_train, brain_train, validation_data=(keystrokes_test, brain_test), epochs=100,
    # batch_size=32)
    #
    # # evaluate the model
    # loss, mae = model.evaluate(keystrokes_test, brain_test)
    # print('Test loss:', loss)
    # print('Test MAE:', mae)

    # LSTM model
    # initialize the model
    model = Sequential()

    # add input layer with 32 units and a 'relu' activation function
    model.add(Dense(32, input_dim=keystrokes_train.shape[1], activation='relu'))

    # add a hidden layer with 16 units and a 'relu' activation function
    model.add(Dense(16, activation='relu'))

    # add LSTM layer with 16 units
    model.add(LSTM(16))

    # add output layer with number of units equal to the number of features in brain_data
    # use linear activation function for regression problem, for classification problem use 'sigmoid' or 'softmax'
    model.add(Dense(brain_train.shape[1], activation='linear'))

    # compile the model
    model.compile(loss='mse', optimizer=Adam(), metrics=['mae'])
    # mean squared error loss for regression problem, for classification problem use 'binary_crossentropy' or
    # 'categorical_crossentropy'

    # train the model
    history = model.fit(keystrokes_train, brain_train, validation_data=(keystrokes_test, brain_test), epochs=100,
                        batch_size=32)

    # evaluate the model
    loss, mae = model.evaluate(keystrokes_test, brain_test)
    print('Test loss:', loss)
    print('Test MAE:', mae)

    # save the model
    model.save('brain_model.h5')

if __name__ == '__main__':
    train_model()
