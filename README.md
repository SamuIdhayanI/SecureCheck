# 🚨 SecureCheck: Digital Police Check Post Registry

SecureCheck is an advanced digital police check post registry system designed to modernize and secure check post operations through real-time data analytics, centralized logging, and predictive insights. This project replaces inefficient manual systems with a robust SQL-backed architecture and a Python-powered Streamlit dashboard.

## 📌 Overview

Manual logging of vehicle checks can lead to inefficiencies and missed threats. **SecureCheck** solves this by:
- Providing a centralized SQL-based database for all police stop records.
- Offering real-time insights through a Streamlit dashboard.
- Enabling predictive analytics for violations and outcomes.
- Supporting crime pattern analysis for improved law enforcement coordination.

---

## 🧾 Dataset

- `traffic_stops_with_vehicle_number.csv`  
  Contains real-world traffic stop data, including columns:
  - `stop_date`, `stop_time`, `country_name`, `driver_gender`, `driver_age_raw`, `driver_age`, `driver_race`, `violation_raw`, `violation`, `search_conducted`, `search_type`, `stop_outcome`, `is_arrested`, `stop_duration`, `drugs_related_stop`, `vehicle_number`.

---

## 📁 Project Structure

```bash
├── traffic_stops_with_vehicle_number.csv        # Dataset
├── data_prep_and_sql_initial.ipynb              # Data cleaning & SQL DB setup
├── app.py                                       # Streamlit app launcher
├── home.py                                      # Home page with metrics & data preview
├── fundamental_insights.py                      # Basic insights (tables + charts)
├── profound_insights.py                         # Advanced analytics (tables + charts)
├── add_log.py                                   # Add new log + prediction logic
├── db_utils.py                                  # MySQL database connection handler
````

---

## 🖥️ Streamlit Dashboard Pages

### 🏠 Home

* Project introduction and dashboard metrics:

  * Total Police Stops
  * Searches Conducted
  * Arrests Made
  * Tickets Issued
* Live data preview

### 💡 Fundamental Insights

* Core statistics and visuals derived from SQL queries
* Tables and visualizations (bar charts, line graphs, etc.)

### 🧠 Profound Insights

* Advanced analytical queries and trend analysis
* Crime pattern detection and visual reports

### 📝 Add New Police Log

* Form to add a new police stop entry
* Predicts:

  * **Violation Type**
  * **Stop Outcome**
* Shows a summary of the newly added entry

---

## ⚙️ Tech Stack

* **Python** (Data processing, Streamlit app)
* **MySQL** (Centralized database)
* **Pandas** (Data manipulation)
* **Plotly** (Data visualization)
* **Streamlit** (Frontend dashboard)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SamuIdhayanI/SecureCheck.git
```

### 2. Set Up Environment

Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

Run the Jupyter notebook to:

* Clean the dataset
* Create MySQL tables
* Insert cleaned data into the database

```bash
jupyter notebook data_prep_and_sql_initial.ipynb
```

### 4. Launch the App

```bash
streamlit run app.py
```

---

## 📸 Dashboard Preview

<img width="1680" alt="image" src="https://github.com/user-attachments/assets/1e6b2232-1176-4da0-a043-878fb3aa0cbe" />



<img width="1680" alt="image" src="https://github.com/user-attachments/assets/53c92ec7-21a0-4065-bc7f-3a88d92c3a7c" />
<img width="1680" alt="image" src="https://github.com/user-attachments/assets/e9455e89-5dc6-4964-a81c-fd529917b319" />



<img width="1679" alt="image" src="https://github.com/user-attachments/assets/11ecec5a-d50c-4ab3-ba9a-b24973ef7d50" />
<img width="1680" alt="image" src="https://github.com/user-attachments/assets/2dc2bb8a-ee1b-40a2-a2fa-44a21be79e95" />

---

