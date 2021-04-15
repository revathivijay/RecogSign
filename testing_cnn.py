import numpy as np
import pandas as pd

from PIL import Image
import cv2

import os
import warnings

from keras.models import model_from_json
from sklearn.metrics import accuracy_score
warnings.filterwarnings("ignore")

## MODEL PATHS
MODEL_JSON_PATH = 'model_new_200.json'
MODEL_WEIGHTS_PATH = 'model_new_200.f5'

## TEST DATA PATH
TEST_FOLDER = 'PeePee/'
TEST_CSV_PATH = 'Test.csv'

# DIMENSIONS OF IMAGE
HEIGHT = 32
WIDTH = 32

def prepare_test_data(TEST_FOLDER=TEST_FOLDER, TEST_CSV_PATH=TEST_CSV_PATH):
    print("The test folder has: ", len(TEST_FOLDER), " images.")
    test_df = pd.read_csv(TEST_CSV_PATH)
    test_df = test_df.drop(labels=['Width', 'Height', 'Roi.X1', 'Roi.Y1', 'Roi.X2', 'Roi.Y2'], axis=1)

    # removing "Test/" from df values
    test_df['Path'] = test_df['Path'].str[5:]

    #dropping rows that aren't in our test set
    for index, item in test_df.iterrows():
        if item[1] not in os.listdir(TEST_FOLDER):
            test_df = test_df.drop(index)
    
    labels = test_df['ClassId'].values
    imgs = test_df["Path"].values

    test_data = []

    for img_temp in imgs:
        try:
            image = cv2.imread(TEST_FOLDER + img_temp)
            image_fromarray = Image.fromarray(image)
            resize_image = image_fromarray.resize((HEIGHT, WIDTH))
            test_data.append(np.array(resize_image))
        except:
            print("Error in loading test image")
        
    X_test = np.array(test_data)
    return X_test, labels


def load_model(MODEL_JSON_PATH=MODEL_JSON_PATH, MODEL_WEIGHTS_PATH=MODEL_WEIGHTS_PATH):
    try:
        json_file = open(MODEL_JSON_PATH, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)

        # load weights into new model  
        loaded_model.load_weights(MODEL_WEIGHTS_PATH)
        return loaded_model
    
    except Exception:
        print("Error loading model!")
        return


# DRIVER CODE
if __name__=='__main__':
    model = load_model()
    test_data, labels = prepare_test_data()
    
    predictions = model.predict_classes(test_data)
    
    #Accuracy with the test data
    print("Accuracy: ", accuracy_score(labels, predictions))


