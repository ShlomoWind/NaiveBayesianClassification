from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Dict,Any
import pandas as pd
from starlette import status

from data_module.Data_Loader import DataLoader
from cleaning_module.Cliner import clean_data
from classification_module.Classification import train,predict

app = FastAPI()

model_class_probs = None
model_probabilities = None
model_features = None

class DataRequest(BaseModel):
    path: str
    type: str
    target: str

class PredictRequest(BaseModel):
    prediction :Dict[str,Any]

@app.post("/train")
def train_data(req:DataRequest):
    global model_class_probs,model_probabilities,model_features
    try:
        loader = DataLoader(req.type,req.path)
        df = loader.load()
        df = clean_data(df)
        df.set_index(req.target, inplace=True)
        model_class_probs,model_probabilities = train(df)
        model_features = list(df.columns)
        return {"message": "Model trained successfully."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/predict")
def user_predict(req:PredictRequest):
    try:
        req_dict = req.prediction
        for feature in model_features:
            if feature not in req_dict:
                raise HTTPException(status_code=400, detail=f"Missing feature: {feature}")
        prediction = predict(req_dict,model_class_probs,model_probabilities)
        return {"prediction":prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))