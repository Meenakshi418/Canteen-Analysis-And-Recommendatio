from fastapi import APIRouter
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from ml.apriori import run_apriori
from ml.clustering import perform_clustering
from ml.preprocessing import load_and_preprocess

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

    result, model, silhouette = perform_clustering(df)

    summary = result.groupby("Cluster")[
        ["Quantity_Sold", "Food_Waste", "Students_Count", "Rating"]
    ].mean().reset_index()

    return {
        "clusters": [
            {
                "cluster": int(row["Cluster"]),
                "silhouette_score": round(float(silhouette), 4),
                "quantity_sold": round(float(row["Quantity_Sold"]), 2),
                "food_waste": round(float(row["Food_Waste"]), 2),
                "students_count": round(float(row["Students_Count"]), 2),
                "rating": round(float(row["Rating"]), 2)
            }
            for _, row in summary.iterrows()
        ]
    }


@router.get("/model_performance")
def model_performance():

    df = load_and_preprocess(DATA_PATH)

    from sklearn.preprocessing import OneHotEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, r2_score

    regression_features = [
        "Students_Count",
        "Quantity_Prepared",
        "Price",
        "Day",
        "Meal_Time",
        "Category",
        "Weather",
        "Special_Event"
    ]

    X = df[regression_features]
    y = df["Quantity_Sold"]

    categorical = [
        "Day",
        "Meal_Time",
        "Category",
        "Weather",
        "Special_Event"
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

    regression_model = Pipeline([
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    regression_model.fit(X_train, y_train)

    predictions = regression_model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    classification_df = df.copy()

    categorical_columns = [
        "Day",
        "Meal_Time",
        "Category",
        "Weather",
        "Special_Event"
    ]

    for column in categorical_columns:
        encoder = LabelEncoder()
        classification_df[column] = encoder.fit_transform(
            classification_df[column].astype(str)
        )

    classification_features = [
        "Students_Count",
        "Day",
        "Meal_Time",
        "Category",
        "Weather",
        "Special_Event"
    ]

    X_class = classification_df[classification_features]
    y_class = classification_df["Demand_Level"].astype(str)

    X_train, X_test, y_train, y_test = train_test_split(
        X_class,
        y_class,
        test_size=0.2,
        random_state=42
    )

    decision_tree = DecisionTreeClassifier(
        criterion="entropy",
        max_depth=5,
        random_state=42
    )

    decision_tree.fit(X_train, y_train)

    tree_predictions = decision_tree.predict(X_test)

    tree_accuracy = accuracy_score(
        y_test,
        tree_predictions
    )

    naive_bayes = GaussianNB()

    naive_bayes.fit(X_train, y_train)

    nb_predictions = naive_bayes.predict(X_test)

    nb_accuracy = accuracy_score(
        y_test,
        nb_predictions
    )

    knn = KNeighborsClassifier(
        n_neighbors=5
    )

    knn.fit(X_train, y_train)

    knn_predictions = knn.predict(X_test)

    knn_accuracy = accuracy_score(
        y_test,
        knn_predictions
    )

    random_forest = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    random_forest.fit(X_train, y_train)

    rf_predictions = random_forest.predict(X_test)

    rf_accuracy = accuracy_score(
        y_test,
        rf_predictions
    )

    result, model, silhouette = perform_clustering(df)

    frequent_items, rules = run_apriori(TRANSACTION_PATH)

    if len(rules) > 0:

        best_rule = rules.sort_values(
            by="lift",
            ascending=False
        ).iloc[0]

        apriori_result = {
            "support": round(float(best_rule["support"]), 4),
            "confidence": round(float(best_rule["confidence"]), 4),
            "lift": round(float(best_rule["lift"]), 4)
        }

    else:

        apriori_result = {
            "support": 0,
            "confidence": 0,
            "lift": 0
        }

    return {
        "regression": {
            "r2_score": round(float(r2), 4),
            "mae": round(float(mae), 2)
        },
        "classification": {
            "decision_tree_accuracy": round(float(tree_accuracy), 4),
            "naive_bayes_accuracy": round(float(nb_accuracy), 4),
            "knn_accuracy": round(float(knn_accuracy), 4),
            "random_forest_accuracy": round(float(rf_accuracy), 4)
        },
        "clustering": {
            "silhouette_score": round(float(silhouette), 4)
        },
        "apriori": apriori_result
    }