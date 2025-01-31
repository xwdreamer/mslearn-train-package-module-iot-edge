# This script generates the scoring file
# with the init and run functions needed to 
# operationalize the anomaly detection sample
# 上面的writefile就是写文件的意思，将先的内容保存到iot_scory.py这个文件当中

import pickle
import json
import pandas
import joblib
from sklearn.linear_model import Ridge
from azureml.core.model import Model

def init():
    global model
    # this is a different behavior than before when the code is run locally, even though the code is the same.
    model_path = Model.get_model_path('model-demo1.pkl')
    # deserialize the model file back into a sklearn model
    model = joblib.load(model_path)

# note you can pass in multiple rows for scoring
def run(input_str):
    try:
        input_json = json.loads(input_str)
        input_df = pandas.DataFrame([[input_json['machine']['temperature'],input_json['machine']['pressure'],input_json['ambient']['temperature'],input_json['ambient']['humidity']]])
        pred = model.predict(input_df)
        print("Prediction is ", pred[0])
    except Exception as e:
        result = str(e)
        
    if pred[0] == 1:
        input_json['anomaly']=True
    else:
        input_json['anomaly']=False
        
    return [json.dumps(input_json)]
