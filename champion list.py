import sqlite3
import pandas as pd


connection = sqlite3.connect("database.db")


df = pd.read_sql(
    "SELECT * FROM team_stats",
    connection
)


champions = {

    "2010-11": "Dallas Mavericks",
    "2011-12": "Miami Heat",
    "2012-13": "Miami Heat",
    "2013-14": "San Antonio Spurs",
    "2014-15": "Golden State Warriors",
    "2015-16": "Cleveland Cavaliers",
    "2016-17": "Golden State Warriors",
    "2017-18": "Golden State Warriors",
    "2018-19": "Toronto Raptors",
    "2019-20": "Los Angeles Lakers",
    "2020-21": "Milwaukee Bucks",
    "2021-22": "Golden State Warriors",
    "2022-23": "Denver Nuggets",
    "2023-24": "Boston Celtics",
    "2024-25": "Oklahoma City Thunder"

}


df["Champion"] = 0


for season, team in champions.items():

    df.loc[
        (df["SEASON"] == season) &
        (df["TEAM_NAME"] == team),
        "Champion"
    ] = 1




df.to_sql(
    "team_stats",
    connection,
    if_exists="replace",
    index=False
)


connection.close()

