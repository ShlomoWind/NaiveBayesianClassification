import streamlit as st
import requests

# כתובת השרת שלך
base_url = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Naive Bayes Predictor", page_icon="🤖")
st.title("🔍 Naive Bayes Classifier")
st.subheader("בחר ערכים לכל פיצ'ר:")

# 👇 ערכים אפשריים לכל פיצ'ר (עדכן לפי הדאטה שלך)
feature_options = {
    "age": ["youth", "middle_aged", "senior"],
    "income": ["low", "medium", "high"],
    "student": ["yes", "no"],
    "credit_rating": ["fair", "excellent"]
}

# יצירת טופס דינמי עם תפריטים נפתחים
input_data = {}
for feature, options in feature_options.items():
    choice = st.selectbox(f"{feature}:", options)
    input_data[feature] = choice

# כפתור חיזוי
if st.button("🔮 בצע חיזוי"):
    try:
        response = requests.post(base_url, json={"prediction": input_data})
        if response.status_code == 200:
            result = response.json()["prediction"]
            st.success(f"חיזוי: {result}")
        else:
            st.error(f"שגיאה מהשרת: {response.status_code} - {response.json()}")
    except Exception as e:
        st.error(f"שגיאה בשליחה לשרת: {e}")