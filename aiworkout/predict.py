
from get_data import get_img

import joblib
import numpy as np
from tensorflow.keras.utils import to_categorical

GCP_TEST_PATH = "gs://"
LOCAL_TEST_PATH = "raw_data/test_img"

PATH_TO_LOCAL_MODEL = 'model.joblib'

def get_test_img(data_path):

    X_test , y_test = get_img(data_path)
    num_classes = len(set(y_test))
    y_test = to_categorical(y_test,num_classes)

    return X_test,y_test

def get_model(path_to_joblib):

    model = joblib.load(path_to_joblib)

    return model

def get_result(y,y_pred):

    length = len(y)
    pred_list = []
    for i in range(length):
        if np.argmax(y[i]) == np.argmax(y_pred[i]):
            pred_list.append('True')
        else:
            pred_list.append('False')

    return pred_list


if __name__ == "__main__":
    X_test,y_test = get_test_img(LOCAL_TEST_PATH)
    model = get_model(PATH_TO_LOCAL_MODEL)
    y_pred = model.predict(X_test)
    res = get_result(y_test,y_pred)
    print(res)
