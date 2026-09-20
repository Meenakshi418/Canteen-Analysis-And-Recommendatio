from fastapi import APIRouter
import pandas as pd
from pathlib import Path

router = APIRouter(prefix="/analytics")

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "canteen_data.csv"

def load_data():
    return pd.read_csv(CSV_PATH)

@router.get("/summary")
def summary():

    df = load_data()
    return {
        "total_quantity_sold": int(df["Quantity_Sold"].sum()),
        "total_food_waste": int(df["Food_Waste"].sum()),
        "average_rating": float(df["Rating"].mean())
    }


@router.get("/top_items")
def top_items():

    df = load_data()
    result = (
        df.groupby("Food_Item")["Quantity_Sold"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    return {
        "top_items": [
            {
                "food_item": str(item),
                "quantity": int(quantity)
            }
            for item, quantity in result.items()
        ]
    }


@router.get("/waste")
def waste():

    df = load_data()
    result = df.groupby("Food_Item")["Food_Waste"].sum()
    return {
        "total_waste_per_food_item": [
            {
                "food_item": str(item),
                "waste": int(waste)
            }
            for item, waste in result.items()
        ]
    }


@router.get("/trends")
def trends():

    df = load_data()
    result = df.groupby("Date")["Quantity_Sold"].sum()
    return {
        "total_quantity_sold_per_day": {
            str(date): int(quantity)
            for date, quantity in result.items()
        }
    }