from fastapi import APIRouter
import pandas as pd
from pathlib import Path
from backend.ml.regression import train_regression_model
from backend.ml.classification import train_j48 , train_naive_bayes
from backend.ml.preprocessing import load_and_preprocess

router  = APIRouter(prefix="/prediction")

DIR_PATH = Path(__file__).resolve().parent.parent
CSV_PATH = DIR_PATH / "data" / "canteen_data.csv"

def load_data():
    return pd.read_csv(CSV_PATH)

@router.get("/demand")
def demand(students_count: int,
    quantity_prepared: int,
    price: int,
    day: str,
    meal_time: str,
    category: str,
    weather: str,
    special_event: str
):

    df = load_data()
    model = train_regression_model(df)

    input_data = pd.DataFrame([{
        "Students_Count": students_count,
        "Quantity_Prepared": quantity_prepared,
        "Price": price,
        "Day": day,
        "Meal_Time": meal_time,
        "Category": category,
        "Weather": weather,
        "Special_Event": special_event
    }])

    prediction = model.predict(input_data)[0]

    return {
        "predicted_quantity_sold": round(float(prediction), 2)
    }

@router.get("/demand_level")
def demand_level(
    students_count: int,
    day: str,
    meal_time: str,
    category: str,
    weather: str,
    special_event: str
):
    df = load_and_preprocess(CSV_PATH)
    model, encoders = train_j48(df)

    input_data = pd.DataFrame([{
        "Students_Count": students_count,
        "Day": encoders["Day"].transform([day])[0],
        "Meal_Time": encoders["Meal_Time"].transform([meal_time])[0],
        "Category": encoders["Category"].transform([category])[0],
        "Weather": encoders["Weather"].transform([weather])[0],
        "Special_Event": encoders["Special_Event"].transform([special_event])[0]
    }])

    prediction = model.predict(input_data)[0]

    return {
        "predicted_demand_level": prediction
    }


@router.get("/waste_level")
def waste_level(
    students_count: int,
    quantity_prepared: int,
    day: str,
    meal_time: str,
    category: str,
    weather: str
):
    df = load_data()
    model, encoders = train_naive_bayes(df)

    input_data = pd.DataFrame([{
        "Students_Count": students_count,
        "Quantity_Prepared": quantity_prepared,
        "Day": encoders["Day"].transform([day])[0],
        "Meal_Time": encoders["Meal_Time"].transform([meal_time])[0],
        "Category": encoders["Category"].transform([category])[0],
        "Weather": encoders["Weather"].transform([weather])[0]
    }])

    prediction = model.predict(input_data)[0]

    return {
        "predicted_waste_level": prediction
    }


