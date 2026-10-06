import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


def perform_clustering(df):
    data = df.copy()

    features = [
        "Quantity_Sold",
        "Food_Waste",
        "Students_Count",
        "Rating"
    ]

    X = data[features]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    data["Cluster"] = model.fit_predict(X_scaled)

    # Use a sample for silhouette calculation.
    # This avoids excessive memory usage on deployment servers.
    sample_size = min(2000, len(X_scaled))

    score = silhouette_score(
        X_scaled,
        data["Cluster"],
        sample_size=sample_size,
        random_state=42
    )

    return data, model, score