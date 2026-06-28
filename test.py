import sqlite3
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression



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




model = Pipeline(
    [
        ("scale", StandardScaler()),

        ("model",
         LogisticRegression(
             max_iter=1000
         ))
    ]
)



results = []


seasons = sorted(
    df["SEASON"].unique()
)



for i in range(5, len(seasons)):


    test_season = seasons[i]


    train_seasons = seasons[:i]


    train = df[
        df["SEASON"].isin(train_seasons)
    ]


    test = df[
        df["SEASON"] == test_season
    ]


    X_train = train[features]
    y_train = train["Champion"]


    X_test = test[features]





    model.fit(
        X_train,
        y_train
    )



    

    probs = model.predict_proba(
        X_test
    )[:,1]


    test = test.copy()

    test["Probability"] = probs





    ranking = test.sort_values(
        "Probability",
        ascending=False
    )


    ranking["Rank"] = range(
        1,
        len(ranking)+1
    )



    champion_row = ranking[
        ranking["Champion"] == 1
    ]


    champion_rank = champion_row["Rank"].values[0]


    champion_team = champion_row["TEAM_NAME"].values[0]



    results.append(
        {
            "Season": test_season,
            "Champion": champion_team,
            "Champion Rank": champion_rank
        }
    )



results_df = pd.DataFrame(results)


print(results_df)





print(
    "Average champion rank:",
    results_df["Champion Rank"].mean()
)


print(
    "Top 5 accuracy:",
    (results_df["Champion Rank"] <= 5).mean()
)