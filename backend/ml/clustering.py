import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def perform_clustering(df):

    data = df.copy()

    features = [
        "Quantity_Sold",
        "Food_Waste",
        "Students_Count",
        "Rating"
    ]

    X = data[features]

    #Scalling bcuz all variables have diff ranges (i.e stud in hundreds,rating in 1-5 )
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    data["Cluster"] = model.fit_predict(
        X_scaled
    )

    return data, model


if __name__ == "__main__":

    from pathlib import Path

    backend_folder = Path(__file__).resolve().parent.parent

    csv_path = (
        backend_folder /
        "data" /
        "canteen_data.csv"
    )

    df = pd.read_csv(csv_path)

    df, model = perform_clustering(df)

    print("\nClustering Results")
    print("------------------")

    print(
        df[
            [
                "Food_Item",
                "Quantity_Sold",
                "Food_Waste",
                "Cluster"
            ]
        ].head(20)
    )

    print("\nCluster Counts:")
    print(df["Cluster"].value_counts())

    cluster_summary = df.groupby("Cluster")[
    ["Quantity_Sold", "Food_Waste", "Students_Count", "Rating"]
    ].mean()

    print("\nCluster Summary")
    print(cluster_summary)