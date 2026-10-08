# 🍽️ College Canteen Demand, Waste Analysis & Prediction

A data-driven **College Canteen Analytics and Demand Prediction System** developed using **Data Warehousing and Data Mining** techniques. The project analyzes canteen sales, food waste, student demand, weather and meal-time patterns to generate useful insights and predict future food demand.

The system helps canteen management make better decisions about **food preparation, inventory planning and waste reduction**.

## 🚀 Features

### 📊 Sales & Demand Analysis

* Analyze food items sold across different meal times
* Analyze student demand patterns
* Compare Breakfast, Lunch and Evening demand
* Analyze monthly and weekly trends
* Identify the most frequently sold food items
* Analyze revenue generated from food sales

### 🗑️ Food Waste Analysis

* Track quantity of food wasted
* Calculate waste percentage
* Identify the most wasted food items
* Analyze waste according to meal time
* Analyze the effect of weather on food waste
* Identify patterns that can help reduce unnecessary food preparation

### 🔮 Demand Prediction

* Predict expected food demand
* Use historical student and sales data
* Consider factors such as:

  * Meal time
  * Weather
  * Student count
  * Food item
  * Historical sales patterns

### ⛅ Weather-Based Analysis

The system analyzes the relationship between weather conditions and:

* Student demand
* Quantity sold
* Food waste
* Revenue

### 📈 Data Mining

Data mining techniques are used to discover meaningful patterns in the canteen dataset.

The project also includes classification-based analysis for predicting and analyzing demand patterns.

## 🛠️ Technology Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python
* FastAPI
* REST API

### Database

* PostgreSQL

### Data Analysis

* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* Seaborn

### Data Mining

* J48 Decision Tree
* Classification
* Pattern analysis

### Deployment

* Render

## 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │   Canteen Dataset    │
                 │                      │
                 │ Sales • Waste •      │
                 │ Weather • Students   │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │   PostgreSQL DB      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     FastAPI          │
                 │      Backend         │
                 └──────────┬───────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌───────────┐
        │ Analytics│  │  Mining  │  │ Prediction│
        └────┬─────┘  └────┬─────┘  └─────┬─────┘
             │             │              │
             └─────────────┼──────────────┘
                           ▼
                 ┌──────────────────────┐
                 │ Analytics Dashboard  │
                 │                      │
                 │ Demand • Waste •      │
                 │ Sales • Predictions  │
                 └──────────────────────┘
```

## 📚 Dataset

The project uses a canteen dataset containing **10,000 records** covering the year **2025**.

Important attributes include:

| Attribute        | Description                 |
| ---------------- | --------------------------- |
| Meal_Time        | Breakfast, Lunch or Evening |
| Food_Items       | Food item sold              |
| Weather          | Weather condition           |
| Students_Count   | Number of students          |
| Quantity_Sold    | Quantity of food sold       |
| Waste            | Quantity of food wasted     |
| Revenue          | Revenue generated           |
| Year             | Year of transaction         |
| Month            | Month of transaction        |
| Week             | Week of transaction         |
| Waste_Percentage | Percentage of food wasted   |

## 📈 Dataset Statistics

| Metric              |   Result |
| ------------------- | -------: |
| Total Records       |   10,000 |
| Total Quantity Sold |  862,977 |
| Total Food Waste    |  412,034 |
| Average Rating      |   4.0017 |
| Most Sold Item      | Vada Pav |
| Most Wasted Item    |   Coffee |

## 🍴 Demand Analysis

Average quantity sold according to meal time:

| Meal Time | Average Quantity Sold |
| --------- | --------------------: |
| Breakfast |                80.619 |
| Evening   |                81.332 |
| Lunch     |                97.222 |

The analysis indicates that **Lunch has the highest average demand**, followed by Evening and Breakfast.

## 🗑️ Waste Analysis

The system analyzes food waste at multiple levels, including:

* Food item
* Meal time
* Weather
* Student count
* Month
* Week

The analysis helps identify food items and conditions associated with higher waste levels.

**Coffee** was identified as the most wasted food item in the analyzed dataset.

## 🤖 Prediction & Data Mining

A **J48 Decision Tree-based classification model** is used for demand-related analysis.

The model achieved an improvement from approximately:

```text
Initial Accuracy  → 80.95%
Improved Accuracy → 84.95%
```

The model can be used to identify demand patterns from historical canteen data and support better food preparation decisions.

## 🔄 Data Processing Workflow

```text
Raw Canteen Data
       ↓
Data Cleaning
       ↓
Data Transformation
       ↓
PostgreSQL Database
       ↓
Data Warehouse
       ↓
OLAP / Analytics
       ↓
Data Mining
       ↓
Demand Prediction
       ↓
Waste Analysis
       ↓
Decision Support
```

## 📁 Project Structure

```text
Canteen-Analysis-And-Recommendatio/
│
├── backend/
│   ├── main.py
│   ├── routers/
│   │   ├── analytics.py
│   │   ├── mining.py
│   │   └── prediction.py
│   │
│   ├── models/
│   ├── schemas/
│   └── database/
│
├── data/
│   └── canteen_data.csv
│
├── frontend/
│   ├── index.html
│   ├── css/
│   └── js/
│
├── requirements.txt
└── README.md
```

> Folder names may vary depending on the final project structure.

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Canteen-Analysis-And-Recommendatio
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database and configure the database connection in the environment variables.

Example:

```env
DATABASE_URL=your_postgresql_database_url
```

### 5. Run the FastAPI Backend

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## 🔌 API Modules

### Analytics

Provides endpoints for:

* Sales analysis
* Food item analysis
* Meal-time analysis
* Revenue analysis
* Waste analysis
* Student-demand analysis

### Mining

Provides data mining operations for discovering patterns in the canteen dataset.

### Prediction

Provides demand-related prediction functionality based on historical data.

## 💡 Key Insights

The analysis provides several useful observations:

* **Vada Pav** has the highest sales among the analyzed food items.
* **Coffee** has the highest recorded food waste.
* **Lunch** has the highest average quantity sold.
* Student count is an important factor affecting food demand.
* Weather conditions can influence both demand and waste.
* Historical demand patterns can be used to support food preparation decisions.
* Improved prediction accuracy can help canteen staff prepare quantities closer to expected demand.

## 🎯 Objectives

The main objectives of the project are:

1. Analyze historical canteen sales data.
2. Study student food-demand patterns.
3. Analyze and identify food-waste trends.
4. Study the influence of weather and meal time on demand.
5. Apply data warehousing techniques for analytical processing.
6. Apply data mining techniques to discover useful patterns.
7. Predict food demand using historical data.
8. Support data-driven canteen management.
9. Reduce unnecessary food preparation and food waste.

## 🌱 Benefits

### For Canteen Management

* Better food preparation planning
* Improved inventory management
* Reduced food wastage
* Better understanding of demand
* Improved resource utilization

### For Students

* Better availability of frequently demanded food
* Reduced chances of food shortages
* Improved canteen service planning

## 🔮 Future Scope

The system can be extended with:

* Real-time sales data
* Advanced machine learning models
* Time-series demand forecasting
* Real-time inventory tracking
* Automated food preparation recommendations
* Mobile application integration
* Weather API integration
* Dynamic pricing analysis
* Real-time waste monitoring

## 👩‍💻 Project Information

**Project Title:** College Canteen Demand and Food Waste Analytics Using Data Warehousing and Data Mining

**Domain:** Data Warehousing and Data Mining

**Technologies:** Python, FastAPI, PostgreSQL, JavaScript, Pandas, Scikit-learn

**Deployment:** Render

This project demonstrates how data warehousing, analytics and data mining can be used to transform historical canteen data into actionable insights for **demand prediction and food-waste reduction**.

## 📄 License

This project is developed for academic and educational purposes.
