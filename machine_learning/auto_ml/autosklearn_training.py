import autosklearn.classification
import pandas as pd
from sklearn.model_selection import train_test_split
import sklearn

def auto_train():
    # Load csv file
    df = pd.read_csv('../../test_data/combined_test.csv')
    # Drop any rows with missing values
    df = df.dropna()

    # Split the data into train and test sets
    train = df.sample(frac=0.8, random_state=1)
    test = df.drop(train.index)
    # The y column is KeyStroke, the X columns are all the other columns
    y_train = train['Keystroke']
    X_train = train.drop(columns=['Keystroke'])
    y_test = test['Keystroke']
    X_test = test.drop(columns=['Keystroke'])

    cls = autosklearn.classification.AutoSklearnClassifier()
    cls.fit(X_train, y_train)
    predictions = cls.predict(X_test)
    print("Accuracy score:", sklearn.metrics.accuracy_score(y_test, predictions))


if __name__ == "__main__":
    auto_train()
