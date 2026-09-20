from fastapi import APIRouter
import pandas as pd
from pathlib import Path

from ml.apriori import run_apriori
from ml.clustering import perform_clustering

router = APIRouter(prefix="/mining")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "canteen_data.csv"
TRANSACTION_PATH = BASE_DIR / "data" / "canteen_transactions.csv"

@router.get("/apriori")
def apriori():

    frequent_items, rules = run_apriori(TRANSACTION_PATH)
    frequent_itemsets = []

    for _, row in frequent_items.iterrows():
        frequent_itemsets.append({
            "items": list(row["itemsets"]),
            "support": float(row["support"])
        })

    association_rules = []
    for _, row in rules.iterrows():
        association_rules.append({
            "antecedents": list(row["antecedents"]),
            "consequents": list(row["consequents"]),
            "support": float(row["support"]),
            "confidence": float(row["confidence"]),
            "lift": float(row["lift"])
        })

    return {
        "frequent_itemsets": frequent_itemsets,
        "association_rules": association_rules
    }


@router.get("/clusters")
def clusters():

    df = pd.read_csv(DATA_PATH)
    result, model = perform_clustering(df)

    summary = result.groupby("Cluster")[
        ["Quantity_Sold", "Food_Waste", "Students_Count", "Rating"]
    ].mean().reset_index()

    return {
        "clusters": [
            {
                "cluster": int(row["Cluster"]),
                "quantity_sold": round(float(row["Quantity_Sold"]), 2),
                "food_waste": round(float(row["Food_Waste"]), 2),
                "students_count": round(float(row["Students_Count"]), 2),
                "rating": round(float(row["Rating"]), 2)
            }
            for _, row in summary.iterrows()
        ]
    }