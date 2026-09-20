import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def eda_visualization(file_path):
    df = pd.read_csv(file_path)
    
    sales_by_food = df.groupby("Food_Item")["Quantity_Sold"].sum()

    #Most sold food items
    x1 = sales_by_food.index
    y1 = sales_by_food.values
    plt.bar(x1, y1)
    plt.xlabel("Food Item")
    plt.ylabel("Quantity Sold")
    plt.show()

    average_by_meal = (df.groupby("Meal_Time")["Quantity_Sold"].mean())
    #average demand by meal time
    x2 = average_by_meal.index
    y2 = average_by_meal.values
    plt.bar(x2, y2)
    plt.xlabel("Meal Time")
    plt.ylabel("Quantity Sold Per Meal")
    plt.show()

    average_demand_by_time = df.groupby("Date")["Quantity_Sold"].sum()
    #Quality sold over time
    x3 = average_demand_by_time.index
    y3 = average_demand_by_time.values
    plt.plot(x3, y3)
    plt.xlabel("Date")
    plt.ylabel("Quantity Sold")
    plt.title("Sales Trend")
    plt.xticks(rotation=45)
    plt.show()

    total_food_waste_for_each_item = df.groupby("Food_Item")["Food_Waste"].sum()
    x4 = total_food_waste_for_each_item.index
    y4 = total_food_waste_for_each_item.values
    plt.bar(x4,y4)
    plt.xlabel("Food Item")
    plt.ylabel("Total Food Waste")
    plt.title("Total Food Waste by Food Item")
    plt.xticks(rotation=45)
    plt.show()

    total_food_waste_for_each_meal = df.groupby("Meal_Time")["Food_Waste"].sum()
    x5 = total_food_waste_for_each_meal.index
    y5 = total_food_waste_for_each_meal.values
    plt.bar(x5, y5)
    plt.xlabel("Meal Time")
    plt.ylabel("Total Food Waste")
    plt.title("Total Food Waste by Meal Time")
    plt.show()

    df["Waste_Percentage"] = (
        df["Food_Waste"] / df["Quantity_Prepared"]
    ) * 100
    food_waste_percentage_per_item = df.groupby("Food_Item")["Waste_Percentage"].sum()
    x6 = food_waste_percentage_per_item.index
    y6 = food_waste_percentage_per_item.values
    plt.bar(x6,y6)
    plt.xlabel("Food Item")
    plt.ylabel("Average Waste Percentage (%)")
    plt.title("Average Waste Percentage by Food Item")
    plt.xticks(rotation=45)
    plt.show()

    # Scatter plot: Students vs Quantity Sold
    x7 = df["Students_Count"]
    y7 = df["Quantity_Sold"]
    plt.scatter(x7, y7)
    plt.xlabel("Number of Students")
    plt.ylabel("Quantity Sold")
    plt.title("Students Count vs Quantity Sold")
    plt.show()

     
if __name__ == "__main__":

    backend_folder = Path(__file__).resolve().parent.parent

    csv_path = backend_folder/"data"/"canteen_data.csv"

    results = eda_visualization(csv_path)


        