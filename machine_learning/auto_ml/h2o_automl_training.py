import h2o
from h2o.automl import H2OAutoML
import pandas as pd


def train_bci_prediction():
    # Start the H2O cluster (locally)
    h2o.init()

    # Import a sample binary outcome train/test set into H2O
    # train = h2o.import_file("https://s3.amazonaws.com/erin-data/higgs/higgs_train_10k.csv")
    # test = h2o.import_file("https://s3.amazonaws.com/erin-data/higgs/higgs_test_5k.csv")
    # Load the EEG and keystroke data
    combined = pd.read_csv('../../test_data/combined_test.csv')

    # Split the data into train and test sets
    train = combined.sample(frac=0.8, random_state=1)
    test = combined.drop(train.index)

    # Identify predictors and response
    x = train.columns
    y = "response"
    x.remove(y)

    # For binary classification, response should be a factor
    train[y] = train[y].asfactor()
    test[y] = test[y].asfactor()

    # Run AutoML for 20 base models
    aml = H2OAutoML(max_models=20, seed=1)
    aml.train(x=x, y=y, training_frame=train)

    # View the AutoML Leaderboard
    lb = aml.leaderboard
    lb.head(rows=lb.nrows)


if __name__ == "__main__":
    train_bci_prediction()
