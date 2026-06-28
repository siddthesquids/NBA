import sqlite3
import pandas as pd

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




model = Pipeline(
    [
        ("scale", StandardScaler()),

        ("classifier",
         LogisticRegression(
             max_iter=1000
         ))
    ]
)



all_results = []

seasons = sorted(df["SEASON"].unique())


for i in range(5, len(seasons)):


    test_season = seasons[i]


    print("Predicting:", test_season)



    train = df[
        df["SEASON"].isin(seasons[:i])
    ]


    test = df[
        df["SEASON"] == test_season
    ]



    X_train = train[features]

    y_train = train["Champion"]




    model.fit(
        X_train,
        y_train
    )




    probabilities = model.predict_proba(
        test[features]
    )[:,1]



    test = test.copy()

    test["Championship_Probability"] = probabilities




    ranking = test.sort_values(
        "Championship_Probability",
        ascending=False
    )


    ranking["Rank"] = range(
        1,
        len(ranking)+1
    )



 

    champion = ranking[
        ranking["Champion"] == 1
    ]



    champion_team = champion["TEAM_NAME"].iloc[0]

    champion_rank = champion["Rank"].iloc[0]

    champion_probability = champion[
        "Championship_Probability"
    ].iloc[0]



    all_results.append(
        {
            "Season": test_season,
            "Actual Champion": champion_team,
            "Champion Rank": champion_rank,
            "Champion Probability": champion_probability
        }
    )



    print(
        ranking[
            [
                "TEAM_NAME",
                "Championship_Probability",
                "Rank"
            ]
        ].head(5)
    )

    print("--------------------")





results = pd.DataFrame(all_results)


print(results)


print(
    "Average Champion Rank:",
    results["Champion Rank"].mean()
)


print(
    "Top 5 Accuracy:",
    (results["Champion Rank"] <= 5).mean()
)