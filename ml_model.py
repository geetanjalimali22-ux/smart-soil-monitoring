import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def train_model():

    data = pd.read_csv("soil_dataset.csv")

    X = data[
        [
            "green_percentage",
            "average_hue"
        ]
    ]

    y = data["salinity_stress"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model