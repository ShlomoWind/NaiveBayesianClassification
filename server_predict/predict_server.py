from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
import pandas as pd
from classification_module.predictor import Predictor

class PredictionInput(BaseModel):
    age: str
    income: str
    student: str
    credit_rating: str

app = FastAPI()
model_url = "http://trainer-container:8000"

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        response = requests.get(f"{model_url}/model")
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Model not found on trainer server.")
        model_data = response.json()
        class_probs = model_data["class_probs"]
        probabilities = model_data["probabilities"]
        predictor = Predictor(class_probs, probabilities)

        df = pd.DataFrame([input_data.model_dump()])
        sample_dict = df.iloc[0].to_dict()
        prediction_result = predictor.predict(sample_dict)
        return {"prediction": prediction_result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))