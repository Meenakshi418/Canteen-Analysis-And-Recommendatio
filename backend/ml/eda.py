import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def eda_function(file_path):

    df = pd.read_csv(file_path)

    total_quantity_sold = df["Quantity_Sold"].sum()

    total_food_waste = df["Food_Waste"].sum()

    average_rating = df["Rating"].mean()

    Most_Sold_Food_Item = (
        df.groupby("Food_Item")["Quantity_Sold"]
        .sum()
        .idxmax()
    )

    Most_Wasted_Food_Item = (df.groupby("Food_Item")["Food_Waste"]
    .sum()
    .idxmax())

    Average_Quantity_By_meal = (df.groupby("Meal_Time")["Quantity_Sold"].mean())

    return {
            "total_quantity_sold":total_quantity_sold,
            "total_food_waste": total_food_waste ,
            "average_rating": average_rating,
            "Most_Sold_Food_Item":Most_Sold_Food_Item ,
            "Most_Wasted_Food_Item": Most_Wasted_Food_Item,
            "Average_Quantity_By_meal": Average_Quantity_By_meal,
        }


if __name__=="__main__":

    backend_folder = Path(__file__).resolve().parent.parent

    csv_path = backend_folder/"data"/"canteen_data.csv"

    results = eda_function(csv_path)

    print(results)

    
    
