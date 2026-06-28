from nba_api.stats.endpoints import leaguedashteamstats
import pandas as pd
import sqlite3
import time
connection = sqlite3.connect("database.db")
allseasons = []
for season in range(2010,2025):
    season_str = f"{season}-{str(season+1)[-2:]}"
    stats = leaguedashteamstats.LeagueDashTeamStats(
        season=season_str,
        season_type_all_star="Regular Season",
        measure_type_detailed_defense="Advanced",
        per_mode_detailed="PerGame"
    )

    df = stats.get_data_frames()[0]

    df = df[
        [
            "TEAM_NAME",
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
    ]

    df["SEASON"] = season_str
    allseasons.append(df)
    time.sleep(1)  

final_df = pd.concat(
    allseasons,
    ignore_index=True
)



final_df.to_sql(
    "team_stats",
    connection,
    if_exists="replace",
    index=False
)


connection.close()

print(df)
print(df.columns)
print(df.columns.tolist()) 
