# 📊 US Insurance Investment Analytics Dashboard

<p align="center">
  <img src="assets/logo/logo.png" alt="Project Logo" width="250"/>
</p>

<p align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)
![phpMyAdmin](https://img.shields.io/badge/phpMyAdmin-6C78AF?style=for-the-badge\&logo=phpmyadmin\&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge\&logo=plotly\&logoColor=white)

</p>

---

# 🌍 US Insurance Investment Analytics Dashboard

An interactive Business Intelligence (BI) dashboard built using **Python, Streamlit, MySQL, phpMyAdmin, Pandas, and Plotly** for analyzing insurance investment portfolios across the United States.

The dashboard enables users to explore insurance records, monitor investment performance, evaluate portfolio distribution, and gain actionable insights through interactive visualizations.

---

# 🚀 Live Demo

**Application URL**

```text
[Add your deployment URL here]
```

---

# 📌 Project Overview

The insurance industry generates large volumes of operational and financial data. Transforming this data into meaningful insights is essential for effective decision-making.

This project was developed to demonstrate how modern data analytics tools can be combined to create an interactive business intelligence solution.

The dashboard allows users to:

* Analyze investment distributions
* Explore insurance records by region
* Evaluate business categories
* Monitor portfolio performance
* Track investment targets
* Visualize insurance risk data
* Generate insights from structured datasets

The project utilizes a synthetic insurance dataset generated programmatically to simulate real-world insurance business scenarios across different U.S. regions.

---

# 🎯 Project Objectives

* Build an end-to-end analytics solution using Streamlit and MySQL.
* Demonstrate database integration in Python.
* Create interactive dashboards for business users.
* Apply descriptive analytics techniques to insurance data.
* Visualize investment trends across geographical locations.
* Showcase business intelligence and dashboard development skills.

---

# ⭐ Key Features

### 📈 Interactive Analytics Dashboard

* Real-time filtering
* Dynamic data exploration
* Responsive dashboard layout

### 📊 KPI Monitoring

Displays:

* Total Investment
* Average Investment
* Median Investment
* Investment Mode
* Portfolio Rating Summary

### 🎯 Investment Progress Tracking

* Investment benchmark monitoring
* Progress indicator
* Animated KPI progress bar

### 🌎 Regional Analysis

Filter by:

* Region
* State
* Location
* Construction Type

### 📋 Interactive Data Viewer

* View insurance records
* Select displayed columns
* Dynamic table filtering

### 📉 Advanced Visualizations

Includes:

* Investment by Business Type (Bar Chart)
* Investment by State (Line Chart)
* Regional Investment Concentration (Treemap)
* Construction Market Share (Donut Chart)

---

# 🏗️ System Architecture

```text
┌────────────────────┐
│   Streamlit UI     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ Python Application │
│ Business Logic     │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ MySQL Database     │
│ salesdb            │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ phpMyAdmin         │
│ Database Manager   │
└────────────────────┘
```

---

# 🗄️ Database Structure

Database:

```sql
salesdb
```

Table:

```sql
us_insurance_analytics_data
```

### Table Schema

| Column       | Data Type              |
| ------------ | ---------------------- |
| Policy       | INT(6)                 |
| Expiry       | VARCHAR(9)             |
| Location     | VARCHAR(5)             |
| State        | VARCHAR(14)            |
| Region       | VARCHAR(9)             |
| Investment   | INT(8)                 |
| Construction | VARCHAR(11)            |
| BusinessType | VARCHAR(11)            |
| Earthquake   | VARCHAR(1)             |
| Flood        | VARCHAR(1)             |
| Rating       | DECIMAL(3,1)           |
| id           | INT(11) AUTO_INCREMENT |

---

# 🧠 Synthetic Data Generation

To simulate real-world insurance operations, a custom Python data generation script was developed.

Generated attributes include:

* U.S. Regions
* U.S. States
* Insurance Policies
* Business Categories
* Construction Types
* Investment Amounts
* Earthquake Risk
* Flood Risk
* Portfolio Ratings

### Dataset Characteristics

* 1000 Generated Records
* Geographic Distribution Across U.S.
* Risk-Based Insurance Attributes
* Realistic Investment Ranges
* Business-Specific Investment Profiles

---

# 📊 Dashboard Analytics

## Home Page

### KPI Summary Cards

* Total Investment
* Investment Mode
* Average Investment
* Median Investment
* Rating Summary

### Interactive Table

Users can:

* View all records
* Select specific columns
* Filter records dynamically

---

## Progress Page

### Investment Target Tracker

Benchmark Target:

```text
$5,000,000,000
```

Displays:

* Progress Percentage
* Completion Status
* Animated Progress Bar

---

### Visual Analytics

#### Investment by Business Type

Provides insights into:

* Retail investments
* Medical investments
* Hospitality investments
* Office building investments

#### Investment Trends by State

Identifies:

* High-performing states
* Regional investment patterns

#### Investment Concentration Treemap

Visual hierarchy of:

```text
Region → State → Investment
```

#### Construction Market Share

Breakdown of investment allocation by:

* Frame
* Fire Resist
* Masonry

---

# 📸 Application Screenshots

## Dashboard Overview

![Dashboard](assets/screenshots/dashboard-home.png)

---

## Performance Analytics

![Analytics](assets/screenshots/dashboard-progress.png)

---

## Database Structure

![Database](assets/screenshots/database-schema.png)

---

# 🎥 Project Demonstration

### Video Walkthrough

[▶ Watch Demo Video](assets/demo/project-demo.mp4)

---

# 🛠️ Technologies Used

| Technology            | Purpose                 |
| --------------------- | ----------------------- |
| Python                | Backend Development     |
| Streamlit             | Dashboard Interface     |
| Pandas                | Data Processing         |
| Plotly Express        | Data Visualization      |
| MySQL                 | Database Storage        |
| phpMyAdmin            | Database Administration |
| Numerize              | KPI Formatting          |
| Streamlit Option Menu | Navigation              |

---

# 📂 Project Structure

```text
US-Insurance-Investment-Analytics-Dashboard/
│
├── app.py
├── Query.py
├── generate_dataset.py
│
├── data/
│   ├── Logo.jpg
│   └── US_Insurance_Analytics_Data.csv
│
├── database/
│   ├── schema.sql
│   └── sample_data.sql
│
├── assets/
│   ├── screenshots/
│   │   ├── dashboard-home.png
│   │   ├── dashboard-progress.png
│   │   └── database-schema.png
│   │
│   └── demo/
│       └── project-demo.mp4
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# ⚙️ Installation Guide

### Clone Repository

```bash
git clone https://github.com/yourusername/US-Insurance-Investment-Analytics-Dashboard.git
```

### Navigate to Project

```bash
cd US-Insurance-Investment-Analytics-Dashboard
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Streamlit Application

```bash
streamlit run app.py
```

---

# 📦 Requirements

```txt
streamlit
pandas
plotly
mysql-connector-python
streamlit-option-menu
numerize
```

---

# 🚀 Deployment

## Recommended Deployment Architecture

### Frontend

* Streamlit Community Cloud

### Database

* Railway MySQL
* Aiven MySQL
* PlanetScale MySQL

### Why Not Localhost?

The current application connects using:

```python
host="localhost"
```

When deployed online, localhost will no longer point to your local machine.

Instead, use environment variables:

```python
host=st.secrets["DB_HOST"]
user=st.secrets["DB_USER"]
password=st.secrets["DB_PASSWORD"]
database=st.secrets["DB_NAME"]
```

---

# 🎓 Skills Demonstrated

* Data Analytics
* Business Intelligence
* Dashboard Engineering
* Database Design
* MySQL Integration
* Data Visualization
* Streamlit Development
* Synthetic Data Generation
* KPI Monitoring
* Interactive Reporting

---

# 🔮 Future Improvements

Potential enhancements:

* User Authentication
* Predictive Analytics
* Machine Learning Risk Models
* Export to Excel/PDF
* Automated Reporting
* Cloud Database Integration
* Real-Time Data Streaming

---

# 👨‍💻 Author

**Your Name**

Data Analytics | Business Intelligence | Python Development

LinkedIn: [Add Link]

GitHub: [Add Link]

---

# ⭐ If you found this project useful

Consider giving it a star on GitHub and sharing it with others interested in Data Analytics and Business Intelligence.
