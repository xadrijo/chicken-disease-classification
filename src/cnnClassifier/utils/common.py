import os
from box.exceptions import BoxValueError
import yaml
from cnnClassifier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Read a yaml file and returns

    Args:
        path_to_yaml (Path): Path to the yaml file
    
    Raises:
        ValueError: if the yaml file is empty
        e: empty file
    
    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml, "r") as f:
            config = yaml.safe_load(f)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(config)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """create list of directories
    
    Args:
        path_to_directories (list): list of directories to create
        verbose (bool, optional): if True, print the directories created. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"directory: {path} created successfully")

@ensure_annotations
def save_json(path: Path, data: dict):
    """Save json data

    Args:
        path (Path): Path to the json file
        data (dict): data to save in json file
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

    logger.info(f"json file: {path} saved successfully")

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load json data

    Args:
        path (Path): Path to the json file
    
    Returns:
        ConfigBox: ConfigBox type
    """
    with open(path, "r") as f:
        data = json.load(f)
        
    logger.info(f"json file: {path} loaded successfully")
    return ConfigBox(data)


@ensure_annotations
def save_bin(data: Any, path: Path):
    """Save binary file

    Args:
        data (Any): data to save in binary file
        path (Path): Path to the binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file: {path} saved successfully")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load binary file

    Args:
        path (Path): Path to the binary file
    
    Returns:
        Any: data loaded from binary file
    """
    data = joblib.load(path)
    logger.info(f"binary file: {path} loaded successfully")

    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """Get size in KB
    
    Args:
        path (Path): Path to the file
        
    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"

def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()

def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, 'rb') as f:
        imgdata = f.read()
    return base64.b64encode(imgdata).decode('utf-8')
