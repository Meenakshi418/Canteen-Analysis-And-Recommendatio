import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


def train_regression_model(df):

    features = [
        "Students_Count",
        "Quantity_Prepared",
        "Price",
        "Day",
        "Meal_Time",
        "Category",
        "Weather",
        "Special_Event"
    ]

    X = df[features]
    y = df["Quantity_Sold"]

    categorical = [
        "Day",
        "Meal_Time",
        "Category",
        "Weather",
        "Special_Event"
    ]

    numerical = [
        "Students_Count",
        "Quantity_Prepared",
        "Price"
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore"),
                categorical
            )
        ],
        remainder="passthrough"
    )

    model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    r2 = r2_score(
        y_test,
        predictions
    )

    print("Regression Results")
    print("------------------")
    print("MAE:", round(mae, 2))
    print("R2 Score:", round(r2, 2))

    return model


# Run regression when this file is executed directly
if __name__ == "__main__":

    from preprocessing import load_and_preprocess
    from pathlib import Path

    backend_folder = Path(__file__).resolve().parent.parent

    csv_path = (
        backend_folder /
        "data" /
        "canteen_data.csv"
    )

    df = load_and_preprocess(csv_path)

    train_regression_model(df)