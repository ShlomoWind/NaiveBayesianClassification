import streamlit as st
import pandas as pd
import requests
import tempfile

API_URL = "http://127.0.0.1:8000"

# הגדרות עמוד
st.set_page_config(
    page_title="🧠 Naive Bayes Classifier",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 מערכת סיווג נאיבי - Naive Bayes Classifier")

# סרגל צד לבחירת פעולה
st.sidebar.header("💡 תפריט")
section = st.sidebar.radio("בחר פעולה:", ["אימון מודל", "חיזוי חדש"])

if section == "אימון מודל":
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
                    # שמירה במצב ישיבה
                    st.session_state["features"] = model_features
                    st.session_state["model_ready"] = True
                    st.experimental_rerun()  # ריענון כדי לעבור למצב חיזוי
                else:
                    st.error(f"🚫 שגיאה באימון המודל: {res.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"🚫 שגיאה בטעינת הקובץ: {str(e)}")

elif section == "חיזוי חדש":
    if not st.session_state.get("model_ready", False):
        st.warning("⚠️ תחילה עליך לאמן את המודל דרך לשונית 'אימון מודל'.")
    else:
        st.header("🔮 הזן ערכים לחיזוי")

        user_input = {}
        with st.form("prediction_form"):
            for feature in st.session_state["features"]:
                # שימוש ב-selectbox לדוגמא - אפשר להרחיב לשדות מתקדמים יותר
                user_input[feature] = st.text_input(f"הכנס ערך עבור '{feature}'")
            submitted = st.form_submit_button("📤 בצע חיזוי")

        if submitted:
            # בדיקה שכל השדות מלאים
            if any(v.strip() == "" for v in user_input.values()):
                st.error("⚠️ יש למלא את כל השדות לפני שליחת החיזוי.")
            else:
                prediction_payload = {"prediction": user_input}
                res = requests.post(f"{API_URL}/predict", json=prediction_payload)
                if res.status_code == 200:
                    st.success(f"✅ התחזית: **{res.json()['prediction']}**")
                else:
                    st.error(f"🚫 שגיאה בתחזית: {res.json().get('detail', 'Unknown error')}")