from fastapi import FastAPI, HTTPException
from data_module.data_loader import DataLoader
from cleaning_module.cleaner import clean_data
from classification_module.train_model import TrainModel
from sklearn.model_selection import train_test_split
from classification_module.predictor import Predictor
from testing_module.tester import accuracy_check

import os
import json
import pandas as pd

app =FastAPI()
model_path = "model_output/model.json"

@app.on_event("startup")
def train_on_startup():
    try:
        target_column = "buys_computer"
        data_loader = DataLoader("csv", "buy_computer_data.csv")
        df = data_loader.load()
        df = clean_data(df)
        df.set_index(target_column, inplace=True)
        train_df, test_df = train_test_split(df, test_size=0.3, random_state=42, stratify=df.index)
        trainer = TrainModel()
        class_probs, probabilities = trainer.train(train_df)
        model_to_save ={
            "class_probs": class_probs,
            "probabilities": probabilities
        }
        os.makedirs("model_output", exist_ok=True)
        with open(model_path, "w") as f:
            json.dump(model_to_save, f)
        predictor = Predictor(class_probs, probabilities)
        accuracy = accuracy_check(test_df, predictor)

        return {
            "message": "Model trained and saved successfully.",
            "accuracy": accuracy
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model")
def get_model():
    try:
        if not os.path.exists(model_path):
            raise HTTPException(status_code=404, detail="Model file not found.")
        with open(model_path, "r") as f:
            model = json.load(f)
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))