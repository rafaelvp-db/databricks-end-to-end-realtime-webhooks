"""Helper class for loading model artifacts. 
Feel free to replace pickle with the serialization library of choice.
"""

from os import path
import pickle

def load_model(model_artifact_path: str):
    """Loads model artifact from the specified path."""

    if (path.exists(model_artifact_path)):
        with open(model_artifact_path, 'rb') as file:
            model_artifact = pickle.load(file)
        return model_artifact
    else:
        raise FileNotFoundError("The specified path ({model_artifact_path})\
            does not exist.")