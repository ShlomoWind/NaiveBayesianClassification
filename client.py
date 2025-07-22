import requests

base_url = "http://127.0.0.1:8000"

def send_prediction_request(input_data: dict):
    response = requests.post(f"{base_url}/predict", json={"prediction": input_data})

    if response.status_code == 200:
        print("Prediction:", response.json()["prediction"])
    else:
        print("Error:", response.status_code, response.json())