import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils

def train_bci_prediction():
    # Load the data
    combined = pd.read_csv('./merged_data_7.csv')
    # Print shape of data
    print(combined.shape)

    # Split the data into features (X) and target (y)
    X = combined.drop('target_column', axis=1)  # replace 'target_column' with the actual name of your target column
    y = combined['target_column']

    # Encoding categorical data if necessary
    # If y is categorical, it should be encoded
    encoder = LabelEncoder()
    encoder.fit(y)
    encoded_y = encoder.transform(y)
    # Convert integers to dummy variables (i.e. one hot encoded)
    dummy_y = np_utils.to_categorical(encoded_y)

    # Split the data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, dummy_y, test_size=0.2, random_state=1)

    # Create model
    model = Sequential()
    model.add(Dense(100, input_dim=X_train.shape[1], activation='relu'))  # Adjust input_dim based on the number of input features
    model.add(Dense(50, activation='relu'))
    model.add(Dense(y_train.shape[1], activation='softmax'))  # Output layer nodes = number of classes

    # Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=10)  # Adjust epochs and batch_size as needed

    # Evaluate the model
    scores = model.evaluate(X_test, y_test)
    print(f"Accuracy: {scores[1]*100}")


if __name__ == "__main__":
    print("Training BCI prediction model...")
    train_bci_prediction()
