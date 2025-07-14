# Arecanut-price-predictor
A machine learning web app built with Streamlit to predict future Arecanut prices using Random Forest, featuring data upload, visualization, SQLite integration, and secure login system.
## ✅ Features

- 📁 Upload arecanut price CSV files
- 📂 Store and manage data in an SQLite database
- 📈 Visualize price trends over time and by month
- 🤖 Predict future prices using Random Forest regression
- 🗅️ Simple and clean user interface built with Streamlit
- 🔐 Login system with username and password

---

## 🔠 Technologies Used

| Component         | Technology        |
|------------------|-------------------|
| Programming       | Python            |
| UI Framework      | Streamlit         |
| Database          | SQLite            |
| ML Algorithm      | Random Forest     |
| Libraries         | pandas, sklearn, joblib, matplotlib |

---

## 🗃️ Dataset Format

Ensure your CSV file contains the following columns:

| Column Name  | Description                      |
|--------------|----------------------------------|
| `date`       | Date of record (YYYY-MM-DD)      |
| `modal_price`| Daily modal price of arecanut    |

---

## 🚀 How to Run the Project

### 🔧 Step 1: Clone or Download the Project

```bash
git clone https://github.com/your-username/arecanut-price-prediction.git
cd arecanut-price-prediction
```

### 📆 Step 2: Install Required Libraries

```bash
pip install -r requirements.txt
```

### ▶️ Step 3: Run the Application

```bash
streamlit run app.py
```

A browser window will open showing your arecanut price prediction app.

---

## 📂 Project Structure

```
ArecanutPricePrediction/
├── app.py                # Main Streamlit app
├── arecanut.db           # SQLite database (auto-generated)
├── sample_data.csv       # Your arecanut price data
├── requirements.txt      # List of Python packages
├── README.md             # Project documentation
├── screenshots/          # Project screenshots
```

---

## 📁 Demo Login Credentials

These are the default credentials to access the application:

| Username   | Password   |
|------------|------------|
| admin      | admin123   |
| preethika  | mca2025    |

> Note: Login is required to access the app features like data upload, visualization, and prediction.

