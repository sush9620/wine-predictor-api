import os
import math
import joblib
import validators
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from wine_predictor_api import api_config, logger
from wine_predictor_api.services.predictor import load_model


def load_data():
    """
    Load Dataset

    :return:
    """
    data_dir_path = api_config.get("data", {}).get("path")
    if not validators.url(data_dir_path) and not os.path.isfile(data_dir_path):
        raise FileNotFoundError("Data path could not be found ")

    return pd.read_csv(data_dir_path)


def train_model():
    """
    Train then save (if efficient) a new machine learning Model based on given dataset

    :return:
    """
    logger.debug("Loading wine data ...")
    dataset = load_data()

    logger.debug("Preparing train and test data ...")
    target = dataset['TARGET']
    features = dataset.drop('TARGET', axis=1)
    x_train, x_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=0)

    logger.debug("Learning model from training set ...")
    linear_model = LinearRegression()
    linear_model.fit(x_train, y_train)

    logger.debug("Evaluating new model ...")
    rmse_new = evaluate_model(model=linear_model, test_data=x_test, test_target=y_test)

    logger.debug("Evaluating old model ...")
    rmse_old = math.inf
    try:
        rmse_old = evaluate_model(model=load_model(), test_data=x_test, test_target=y_test)
    except Exception as exp:
        logger.exception(exp)

    # Save new model as default if more performing than the existing one
    if rmse_new < rmse_old:
        save_model(model=linear_model, output_path=api_config.get("model", {}).get("path"))
        return "New model has been successfully trained and saved as default", 201
    else:
        logger.debug("Discarding model ...")
        return "New model has been successfully trained but discarded (Accuracy does not exceed the existing model)", 200


def evaluate_model(model, test_data, test_target):
    """
    Evaluate the model performance given

    :param model:
    :param test_data:
    :param test_target:

    :return:
    """
    y_predicted = model.predict(test_data)
    mse = mean_squared_error(y_predicted, test_target)
    return mse


def save_model(model, output_path):
    """
    Save the model on the given output path
    :param model:
    :param output_path:
    :return:
    """
    logger.debug(f"Saving model in {output_path}...")
    return joblib.dump(model, output_path)
