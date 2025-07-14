import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import joblib
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# ============================
# 🔐 LOGIN SYSTEM
# ============================
USERS = {
    "admin": "admin123",
    "preethika": "mca2025",
}

def login():
    st.title("🔐 Login to Arecanut Price Predictor")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")

    if login_btn:
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success(f"Welcome, {username} 👋")
            st.rerun()  # ✅ Updated line
        else:
            st.error("❌ Invalid username or password")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# ============================
# 📁 DATABASE SETUP
# ============================
DB_PATH = "arecanut.db"
MODEL_PATH = "model.pkl"

def create_connection():
    return sqlite3.connect(DB_PATH)

def create_table():
    conn = create_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS arecanut_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            modal_price REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_data_from_csv(df):
    conn = create_connection()
    df.to_sql("arecanut_prices", conn, if_exists="append", index=False)
    conn.commit()
    conn.close()

def load_data():
    conn = create_connection()
    df = pd.read_sql_query("SELECT date, modal_price FROM arecanut_prices", conn)
    conn.close()
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    return df

@st.cache_resource
def train_model():
    df = load_data()
    df = df.dropna()
    df['lag_price'] = df['modal_price'].shift(1).fillna(method='bfill')
    X = df[['month', 'lag_price']]
    y = df['modal_price']
    model = RandomForestRegressor()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)
    return model

@st.cache_resource
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except:
        return train_model()

# ============================
# 🌐 STREAMLIT APP START
# ============================
st.title("🌾 Arecanut Price Predictor")
menu = st.sidebar.radio("Navigate", ["Home", "Upload Data", "Visualize", "Predict", "About"])
create_table()

if menu == "Home":
    st.markdown("""
    Welcome to the **Arecanut Price Prediction App** 👋

    - 📁 Upload historical price data
    - 📈 Visualize seasonal trends
    - 🤖 Predict upcoming market prices using ML
    """)

elif menu == "Upload Data":
    uploaded = st.file_uploader("Upload Arecanut Price CSV", type="csv")
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        if 'date' in df.columns and 'modal_price' in df.columns:
            insert_data_from_csv(df)
            st.success("✅ Data uploaded to database successfully!")
        else:
            st.error("❌ CSV must contain 'date' and 'modal_price' columns")

elif menu == "Visualize":
    df = load_data()
    st.subheader("📊 Price Trend Over Time")
    st.line_chart(df.set_index("date")["modal_price"])
    st.subheader("📅 Average Price by Month")
    monthly_avg = df.groupby("month")["modal_price"].mean()
    st.bar_chart(monthly_avg)

elif menu == "Predict":
    model = load_model()
    df = load_data()
    last_price = df['modal_price'].iloc[-1] if not df.empty else 30000
    st.subheader("🧠 Predict Arecanut Price")
    month = st.selectbox("Select Upcoming Month", list(range(1,13)),
                         format_func=lambda x: pd.to_datetime(str(x), format='%m').strftime('%B'))
    lag = st.number_input("Enter Last Known Modal Price", value=float(last_price))
    input_df = pd.DataFrame({"month": [month], "lag_price": [lag]})
    prediction = model.predict(input_df)[0]
    st.success(f"📈 Predicted Arecanut Price: ₹ {prediction:,.2f}")

elif menu == "About":
    st.markdown("""
    ### 📘 Project Info
    - **Title:** Arecanut Price Prediction using Machine Learning
    - **Technology:** Python, Streamlit, SQLite, Random Forest
    - **Database:** SQLite (arecanut.db)
    - **Model:** Random Forest Regressor (model.pkl)
    - **By:** Preethika KS, MCA, New Horizon College of Engineering
    """)

