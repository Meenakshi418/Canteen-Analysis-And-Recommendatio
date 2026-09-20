import psycopg2
import os
from dotenv import load_dotenv
from etl.load_warehouse import transform
from pathlib import Path

backend_folder = Path(__file__).resolve().parent
csv_path = backend_folder / "data" / "canteen_data.csv"

df, dim_date, dim_food, dim_meal, dim_weather, fact_canteen = transform(csv_path)

load_dotenv()
password = os.getenv("password")

#after etl -> load
connection = psycopg2.connect(
    host="localhost",
    database="canteen",
    user="postgres",
    password=password,
    port="5432"
)

print("Database connected successfully!")


def load_dimensions(connection, dataframe, table_name, columns):

    cursor = connection.cursor()

    for _, row in dataframe.iterrows():
        values = tuple(row[column].item() if hasattr(row[column], "item") else row[column] for column in columns)

        placeholders = ", ".join(["%s"] * len(columns))
        column_names = ", ".join(columns)

        query= f"""
            INSERT INTO {table_name}
            ({column_names})
            VALUES ({placeholders})
        """

        cursor.execute(query, values)

    connection.commit()
    cursor.close()

    print(f"{table_name} loaded succesfully")

load_dimensions(
    connection,
    dim_date,
    "Dim_Date",
    ["Date_ID", "Date", "Day", "Week", "Month", "Year"]
)

load_dimensions(
    connection,
    dim_food,
    "Dim_Food",
    ["Food_ID", "Food_Item", "Category", "Price"]
)

load_dimensions(
    connection,
    dim_meal,
    "Dim_Meal",
    ["Meal_ID", "Meal_Time"]
)

load_dimensions(
    connection,
    dim_weather,
    "Dim_Weather",
    ["Weather_ID", "Weather", "Special_Event"]
)

load_dimensions(
    connection,
    fact_canteen,
    "Fact_Canteen",
    ["Students_Count", "Quantity_Prepared", "Quantity_Sold","Food_Waste","Rating", "Fact_ID", "Food_ID", "Weather_ID", "Meal_ID", "Date_ID","Revenue"]
)
connection.close()