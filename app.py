import streamlit as st
import pandas as pd
import requests
import tempfile

# כתובת ה-API שלך
API_URL = "http://127.0.0.1:8000"

st.title("🧠 Naive Bayes Classifier (FastAPI Interface)")

st.header("📁 העלאת קובץ נתונים")
uploaded_file = st.file_uploader("בחר קובץ נתונים", type=["csv", "json", "xlsx"])

file_type = st.selectbox("סוג הקובץ:", ["csv", "json", "excel"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix="." + file_type) as tmp:
        tmp.write(uploaded_file.getbuffer())
        file_path = tmp.name

    try:
        if file_type == "csv":
            df = pd.read_csv(file_path)
        elif file_type == "json":
            df = pd.read_json(file_path)
        elif file_type == "excel":
            df = pd.read_excel(file_path)

        st.success("✔️ קובץ נטען בהצלחה")
        st.dataframe(df)

        target_col = st.selectbox("בחר עמודת יעד לסיווג:", df.columns)

        if st.button("🛠 אמן מודל"):
            train_payload = {
                "path": file_path,
                "type": file_type,
                "target": target_col
            }
            res = requests.post(f"{API_URL}/train", json=train_payload)
            if res.status_code == 200:
                st.success("🎉 המודל אומן בהצלחה!")
                model_features = list(df.columns.drop(target_col))
            else:
                st.error(f"שגיאה באימון המודל: {res.json()['detail']}")
                st.stop()

            st.session_state["features"] = model_features
            st.session_state["model_ready"] = True

    except Exception as e:
        st.error(f"שגיאה בטעינת הקובץ: {str(e)}")

# רק אם המודל אומן
if st.session_state.get("model_ready", False):
    st.header("🔮 תחזית לדוגמה חדשה")

    user_input = {}
    for feature in st.session_state["features"]:
        user_input[feature] = st.text_input(f"הכנס ערך עבור '{feature}'")

    if st.button("📤 בצע חיזוי"):
        prediction_payload = {"prediction": user_input}
        res = requests.post(f"{API_URL}/predict", json=prediction_payload)
        if res.status_code == 200:
            st.success(f"✅ התחזית: **{res.json()['prediction']}**")
        else:
            st.error(f"שגיאה בתחזית: {res.json()['detail']}")