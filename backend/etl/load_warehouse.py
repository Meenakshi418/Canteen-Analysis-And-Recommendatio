import pandas as pd
from pathlib import Path

def extract(file_path):
    df = pd.read_csv(file_path)
    return df

def transform(file_path):
    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Week"] = df["Date"].dt.isocalendar().week

    dim_food = df[["Food_Item","Category","Price"]].drop_duplicates()
    dim_food["Food_ID"] = range(1,len(dim_food)+1)

    dim_meal = df[["Meal_Time"]].drop_duplicates()
    dim_meal["Meal_ID"] = range(1, len(dim_meal)+1)

    dim_weather = df[["Weather", "Special_Event"]].drop_duplicates()
    dim_weather["Weather_ID"] = range(1, len(dim_weather)+1)

    dim_date = df[["Date", "Day", "Week", "Month", "Year"]].drop_duplicates()
    dim_date["Date_ID"] = range(1, len(dim_date)+1)

    fact_canteen = df.copy()
    fact_canteen["Fact_ID"] = range(1, len(fact_canteen) + 1)

    fact_canteen = fact_canteen.merge(
        dim_food[["Food_Item", "Food_ID"]],
        on="Food_Item",
        how="left"
    )

    fact_canteen = fact_canteen.merge(
        dim_weather[["Weather", "Special_Event", "Weather_ID"]],
        on=["Weather", "Special_Event"],
        how="left"
    )

    fact_canteen = fact_canteen.merge(
        dim_meal[["Meal_Time", "Meal_ID"]],
        on="Meal_Time",
        how="left"
    )

    fact_canteen = fact_canteen.merge(
        dim_date[["Date", "Date_ID"]],
        on="Date",
        how="left"
    )
    fact_canteen["Revenue"] = (
        fact_canteen["Quantity_Sold"] * fact_canteen["Price"]
    )
    #remove descriptive columns
    fact_canteen = fact_canteen.drop(columns=[
        "Date",
        "Day",
        "Year",
        "Month",
        "Week",
        "Meal_Time",
        "Food_Item",
        "Category",
        "Weather",
        "Special_Event",
        "Price"
    ])

    print(fact_canteen.shape)
    print(fact_canteen.head())
    print(fact_canteen.columns)
    print(fact_canteen.columns.tolist())

    
    dim_date.to_csv("dim_date.csv", index=False)
    dim_food.to_csv("dim_food.csv", index=False)
    dim_meal.to_csv("dim_meal.csv", index=False)
    dim_weather.to_csv("dim_weather.csv", index=False)
    fact_canteen.to_csv("fact_canteen.csv", index=False)

    return df, dim_date, dim_food, dim_meal, dim_weather, fact_canteen

if __name__ == "__main__":

    backend_folder = Path(__file__).resolve().parent.parent

    csv_path = backend_folder/"data"/"canteen_data.csv"

    results = transform(csv_path)
    print(results)


