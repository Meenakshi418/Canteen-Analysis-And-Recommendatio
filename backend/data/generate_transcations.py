import pandas as pd
import random

random.seed(42)

food_items = [
    "Veg Sandwich",
    "Samosa",
    "Vada Pav",
    "Masala Dosa",
    "Veg Thali",
    "Pav Bhaji",
    "Tea",
    "Coffee",
    "Cold Drink",
    "Idli"
]

transactions = []

for transaction_id in range(1, 5001):

    items = []

    # Randomly choose a primary item
    primary = random.choice(food_items)
    items.append(primary)

    # Realistic purchasing patterns
    if primary == "Samosa":
        if random.random() < 0.70:
            items.append("Tea")

    elif primary == "Veg Sandwich":
        if random.random() < 0.65:
            items.append("Cold Drink")

    elif primary == "Vada Pav":
        if random.random() < 0.60:
            items.append("Cold Drink")

    elif primary == "Masala Dosa":
        if random.random() < 0.65:
            items.append("Tea")

    elif primary == "Idli":
        if random.random() < 0.60:
            items.append("Tea")

    elif primary == "Pav Bhaji":
        if random.random() < 0.55:
            items.append("Cold Drink")

    # Occasionally add another random item
    if random.random() < 0.20:

        extra = random.choice(food_items)

        if extra not in items:
            items.append(extra)

    for item in items:

        transactions.append([
            transaction_id,
            item
        ])


df = pd.DataFrame(
    transactions,
    columns=[
        "Transaction_ID",
        "Food_Item"
    ]
)

df.to_csv(
    "canteen_transactions.csv",
    index=False
)

print("Transaction dataset created")
print("Transactions:", df["Transaction_ID"].nunique())
print("Rows:", len(df))