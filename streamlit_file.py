import streamlit as st
import requests

base_url = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Naive Bayes Predictor", page_icon="🤖")
st.title("🔍 Naive Bayes Classifier")

st.subheader("Select values for each feature:")

feature_options = {
    "age": ["youth", "middle_aged", "senior"],
    "income": ["low", "medium", "high"],
    "student": ["yes", "no"],
    "credit_rating": ["fair", "excellent"]
}

input_data = {}
for feature, options in feature_options.items():
    choice = st.selectbox(f"{feature}:", options)
    input_data[feature] = choice

if st.button("🔮 Predict💡"):
    try:
        response = requests.post(base_url, json={"prediction": input_data})
        if response.status_code == 200:
            result = response.json()["prediction"]
            st.success(f"prediction: {result}")
        else:
            st.error(f"error from the server: {response.status_code} - {response.json()}")
    except Exception as e:
        st.error(f"error sending to server: {e}")