from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any

from data_module.Data_Loader import DataLoader
from cleaning_module.Cleaner import clean_data
from classification_module.train_model import TrainModel
from classification_module.predictor import Predictor

app = FastAPI()

data_path = "buy_computer_data.csv"
data_type = "csv"
target_column = "buys_computer"

model_probabilities = None
model_class_probs = None
model_features = None
predictor = None

class PredictRequest(BaseModel):
    prediction: Dict[str, Any]

try:
    loader = DataLoader(data_type, data_path)
    df = loader.load()
    df = clean_data(df)
    df.set_index(target_column, inplace=True)

    trainer = TrainModel()
    model_class_probs, model_probabilities = trainer.train(df)
    model_features = list(df.columns)

    predictor = Predictor(model_class_probs, model_probabilities)

    print("message: Model trained successfully.")
except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/predict")
def user_predict(req: PredictRequest):
    global predictor, model_features
    if predictor is None:
        raise HTTPException(status_code=400, detail="Model is not trained yet. Please train before predicting.")
    req_dict = req.prediction
    try:
        prediction = predictor.predict(req_dict)
        return {"prediction": prediction}
    except Exception as ex:
        raise HTTPException(status_code=400, detail=str(ex))