import requests

base_url = "http://127.0.0.1:8000"

train_data = {
    "path": "buy_computer_data.csv",
    "type": "csv",
    "target": "buys_computer"}

train_res = requests.post(f"{base_url}/train", json=train_data)

if train_res.status_code == 200:
    print("training successful")
else:
    print("training error", train_res.json())
    exit()

prediction_sample = {
    "prediction": {
        "age": "youth",
        "income": "medium",
        "student": "no",
        "credit_rating": "fair"
    }
}

predict_res = requests.post(f"{base_url}/predict", json=prediction_sample)

if predict_res.status_code == 200:
    print("prediction: ", predict_res.json()['prediction'])
else:
    print("Error ", predict_res.json())