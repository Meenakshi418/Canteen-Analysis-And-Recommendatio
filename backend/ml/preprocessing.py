import pandas as pd
from pathlib import Path


def load_and_preprocess(file_path):

    df = pd.read_csv(file_path)

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows with missing values
    df = df.dropna()

    # Convert Date column
    df["Date"] = pd.to_datetime(df["Date"])

    # Extract year and month
    df["Month"] = df["Date"].dt.month
    df["Year"] = df["Date"].dt.year

    # Calculate waste percentage
    df["Waste_Percentage"] = (
        df["Food_Waste"] / df["Quantity_Prepared"]
    ) * 100

    # Create demand categories
    df["Demand_Level"] = pd.cut(
        df["Quantity_Sold"],
        bins=[-1, 50, 100, float("inf")],
        labels=["Low", "Medium", "High"]
    )

    df["Sales_Percentage"] = (
        df["Quantity_Sold"] / df["Quantity_Prepared"]
    )* 100

    return df


if __name__ == "__main__":

    # Find backend folder automatically
    backend_folder = Path(__file__).resolve().parent.parent

    csv_path = backend_folder / "data" / "canteen_data.csv"

    df = load_and_preprocess(csv_path)

    print(df.head())

    print("\nColumns:")
    print(df.columns)