import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

food_items = {
    "Veg Sandwich": ("Snacks", 40),
    "Samosa": ("Snacks", 20),
    "Vada Pav": ("Snacks", 25),
    "Masala Dosa": ("Meals", 60),
    "Veg Thali": ("Meals", 90),
    "Pav Bhaji": ("Meals", 70),
    "Tea": ("Drinks", 15),
    "Coffee": ("Drinks", 25),
    "Cold Drink": ("Drinks", 30),
    "Idli": ("Breakfast", 35)
}

meal_times = ["Breakfast", "Lunch", "Evening"]
weather_options = ["Sunny", "Cloudy", "Rainy"]
days = ["Monday", "Tuesday", "Wednesday",
        "Thursday", "Friday", "Saturday"]

start_date = datetime(2025, 1, 1)

records = []

for i in range(10000):

    date = start_date + timedelta(days=random.randint(0, 364))

    day = date.strftime("%A")

    meal_time = random.choice(meal_times)

    food_item = random.choice(list(food_items.keys()))

    category, price = food_items[food_item]

    students = random.randint(150, 600)

    weather = random.choice(weather_options)

    special_event = random.choice(["Yes", "No"])

    demand_ratio = random.uniform(0.65, 0.95)

    if meal_time == "Lunch":
        demand_ratio += 0.10

    student_factor = students / 500

    quantity_prepared = int(
        50 + students * demand_ratio * 0.25
    )

    quantity_sold = int(
        quantity_prepared *
        min(demand_ratio * student_factor, 0.98)
    )

    quantity_sold += random.randint(-5, 8)

    quantity_sold = max(
        0,
        min(quantity_sold, quantity_prepared)
    )

    food_waste = quantity_prepared - quantity_sold

    rating = round(
        random.uniform(3.0, 5.0), 1
    )

    records.append([
        date.strftime("%Y-%m-%d"),
        day,
        meal_time,
        food_item,
        category,
        students,
        quantity_prepared,
        quantity_sold,
        food_waste,
        price,
        weather,
        special_event,
        rating
    ])

columns = [
    "Date",
    "Day",
    "Meal_Time",
    "Food_Item",
    "Category",
    "Students_Count",
    "Quantity_Prepared",
    "Quantity_Sold",
    "Food_Waste",
    "Price",
    "Weather",
    "Special_Event",
    "Rating"
]

df = pd.DataFrame(records, columns=columns)

df.to_csv(
    "canteen_data.csv",
    index=False
)

print("Dataset generated successfully!")
print("Rows:", len(df))
print(df.head())