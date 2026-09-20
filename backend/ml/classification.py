import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score


def encode_data(df):

    data = df.copy()

    categorical_columns = [
        "Day",
        "Meal_Time",
        "Category",
        "Weather",
        "Special_Event"
    ]

    encoders = {}

    for column in categorical_columns:
        encoder = LabelEncoder()

        data[column] = encoder.fit_transform(
            data[column].astype(str)
        )

        encoders[column] = encoder

    return data, encoders


# J48 / Decision Tree

def train_j48(df):

    data, encoders = encode_data(df)

    features = [
        "Students_Count",
        "Day",
        "Meal_Time",
        "Category",
        "Weather",
        "Special_Event"
    ]

    X = data[features]

    y = data["Demand_Level"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = DecisionTreeClassifier(
        criterion="entropy",
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\nJ48 / Decision Tree Results")
    print("Accuracy:",
          round(accuracy * 100, 2), "%")

    return model, encoders



# Naive Bayes

def train_naive_bayes(df):

    data, encoders = encode_data(df)

    # Create waste category
    data["Waste_Level"] = pd.cut(
        data["Food_Waste"],
        bins=[-1, 15, float("inf")],
        labels=["Low Waste", "High Waste"]
    )

    features = [
        "Students_Count",
        "Quantity_Prepared",
        "Day",
        "Meal_Time",
        "Category",
        "Weather"
    ]

    X = data[features]

    y = data["Waste_Level"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model = GaussianNB()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\nNaive Bayes Results")
    print("Accuracy:",
          round(accuracy * 100, 2), "%")

    return model, encoders


# Run both models

if __name__ == "__main__":

    from pathlib import Path
    from preprocessing import load_and_preprocess

    backend_folder = Path(__file__).resolve().parent.parent

    csv_path = (
        backend_folder /
        "data" /
        "canteen_data.csv"
    )

    df = load_and_preprocess(csv_path)

    train_j48(df)

    train_naive_bayes(df)