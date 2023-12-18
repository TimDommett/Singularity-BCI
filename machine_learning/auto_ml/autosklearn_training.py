import autosklearn.classification
import pandas as pd
from sklearn.model_selection import train_test_split
import sklearn

def auto_train():
    # Load csv file
    df = pd.read_csv('./merged_data_2.csv')
    # Drop any rows with missing values
    df = df.dropna()

    # Split the data into train and test sets
    train = df.sample(frac=0.8, random_state=1)
    test = df.drop(train.index)
    # Drop Time and time columns
    train = train.drop(columns=['Time', 'time'])
    # The y column is KeyStroke, the X columns are all the other columns
    y_train = train['data']
    X_train = train.drop(columns=['data'])
    y_test = test['data']
    X_test = test.drop(columns=['data'])

    cls = autosklearn.classification.AutoSklearnClassifier(memory_limit=20000)
    cls.fit(X_train, y_train)
    predictions = cls.predict(X_test)
    print("Accuracy score:", sklearn.metrics.accuracy_score(y_test, predictions))


if __name__ == "__main__":
    auto_train()
