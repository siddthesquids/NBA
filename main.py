import sqlite3
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

connection = sqlite3.connect("database.db")
df = pd.read_sql(
    "SELECT * FROM team_stats",
    connection
)


connection.close()
features = [
    "W",
    "L",
    "OFF_RATING",
    "DEF_RATING",
    "NET_RATING",
    "TS_PCT",
    "TM_TOV_PCT",
    "OREB_PCT",
    "DREB_PCT",
    "PACE",
    "EFG_PCT"
]


X = df[features]

y = df["Champion"]
train = df[df["SEASON"] < "2023-24"]

test = df[df["SEASON"] >= "2023-24"]


X_train = train[features]

y_train = train["Champion"]


X_test = test[features]

y_test = test["Champion"]




model = Pipeline(
    [
        ("scale", StandardScaler()),

        ("classifier",
         LogisticRegression(
             max_iter=1000
         ))
    ]
)




model.fit(
    X_train,
    y_train
)




current = df[
    df["SEASON"] == "2024-25"
]


probabilities = model.predict_proba(
    current[features]
)



current["Championship_Probability"] = (
    probabilities[:,1]
)




ranking = current.sort_values(
    "Championship_Probability",
    ascending=False
)


print(
    ranking[
        [
            "TEAM_NAME",
            "Championship_Probability"
        ]
    ]
)