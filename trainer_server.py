from fastapi import FastAPI, HTTPException
from data_module.Data_Loader import DataLoader
from cleaning_module.Cleaner import clean_data
from classification_module.train_model import TrainModel

import os
import json
import pandas as pd

app =FastAPI()
model_path = "model_output/model.json"

@app.post("/train")
def train_model():
    try:
        target_column = "buys_computer"
        data_loader = DataLoader("csv","buy_computer_data.csv")
        df = data_loader.load()
        df = clean_data(df)
        df.set_index(target_column, inplace=True)

        trainer = TrainModel()
        class_probs,probabilities = trainer.train(df)

        model_to_save ={
            "class_probs": class_probs,
            "probabilities": probabilities
        }
        os.makedirs("model_output", exist_ok=True)
        with open(model_path, "w") as f:
            json.dump(model_to_save, f)
        return {"message": "Model trained and saved successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))