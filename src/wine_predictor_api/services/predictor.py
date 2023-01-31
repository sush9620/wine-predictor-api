import os
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression
from wine_predictor_api import api_config, logger


def load_model():
    """
    Load the machine learning model from config file

    :return:
    """
    model_dir_path = api_config.get("model", {}).get("path")
    if not os.path.isfile(model_dir_path):
        raise FileNotFoundError("Model could not be found ")

    return joblib.load(model_dir_path)


def model_predict(data):
    """
    Load the statistical model and predict the quality

    :param data:
    :return:
    """
    logger.debug("Loading ")
    model: LinearRegression = load_model()
    prediction = model.predict(data).tolist()[0]
    if 0 <= prediction <= 10:
        return prediction
    else:
        raise ValueError("Predicted Value out of scale range.")


def prepare_data(data):
    """
    Prepare input data

    :param data:
    :return:
    """
    features = get_features()
    data = [value for key, value in data.items() if key in features]
    data = np.array([data])
    return data


def estimate_wine_quality(**kwargs):
    """
    Service to estimate the quality of a wine from a defined set of features

    :param kwargs:
    :return:
    """
    try:

        data = prepare_data(kwargs)
        logger.debug(f"Data after preparation: {data}")

        predicted = model_predict(data)
        logger.debug(f"Predicted quality: {predicted}")

        predicted_rounded_up = int(round(predicted, 0))
        logger.debug(f"Rounded Predicted quality: {predicted}")

        return {"estimation": predicted_rounded_up}, 200

    except ValueError as value_error:
        logger.error(str(value_error))
        return str(value_error), 500

    except FileNotFoundError as file_not_found_error:
        logger.error(str(file_not_found_error))
        return str(file_not_found_error), 404

    except Exception as ex:
        logger.error(str(ex))
        return "Unexpected Error occurred while predicting value", 500


def get_features():
    """
    Get the list of all features

    :return:
    """
    return ["fixed_acidity",
            "volatile_acidity",
            "citric_acid",
            "residual_sugar",
            "chlorides",
            "free_sulfur_dioxide",
            "total_sulfur_dioxide",
            "density",
            "ph",
            "sulphates",
            "alcohol"]
