import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Conv1D, MaxPooling1D, Flatten, TimeDistributed, Dropout
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load the dataset
print("Loading dataset...")
df = pd.read_csv('../data_for_training/v1/combined_brain_button_data.csv')

# Assuming the first columns are brain data and the last columns are buttons
print("Preparing dataset...")
button_columns = ["DownArrow", "X", "UpArrow", "Square", "L1", "L3", "R3", "R1", "Circle", "Right Options Button",
                  "RightArrow", "LeftArrow", "Triangle", "PlayStation Button", "Middle Button"]
brain_data_columns = [col for col in df.columns if col not in ['Timestamp'] + button_columns + ['data']]


# Prepare the dataset
X = df[brain_data_columns].values
y = df[button_columns].values

# Normalize the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Reshape X for RNN input (samples, time steps, features)
print("Reshaping dataset...")
X = np.reshape(X, (X.shape[0], 1, X.shape[1]))

# Split the dataset
print("Splitting dataset...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the RNN model with a CNN component
print("Creating model...")
model = Sequential()
model.add(TimeDistributed(Conv1D(filters=64, kernel_size=3, activation='relu'), input_shape=(None, X.shape[2], 1)))
model.add(TimeDistributed(MaxPooling1D(pool_size=2)))
model.add(TimeDistributed(Flatten()))
model.add(LSTM(50, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(button_columns), activation='sigmoid'))

# Compile the model
print("Compiling model...")
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
print("Training model...")
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# Save the model
print("Saving model...")
model.save('rnn_cnn_model.h5')

if __name__ == '__main__':
    print("Model training complete. Model saved as 'rnn_cnn_model.h5'")
