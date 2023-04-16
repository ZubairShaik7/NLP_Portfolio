import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('champions_league_database2')
c = conn.cursor()

c.execute(
    'CREATE TABLE IF NOT EXISTS clubs (position number, club text, country text, participated number, titles number, '
    'played number, win number, draw number, loss number, goals_for number, goals_against number, pts number, '
    'goal_diff number)')
conn.commit()

c.execute(
    'CREATE TABLE IF NOT EXISTS players (player number, goals number, appearances number, nationality text, '
    'club text, rating number, height number, weight number, preffered_foot text, birth_date text, age number, '
    'preffered_position text)')
conn.commit()

c.execute(
    'CREATE TABLE IF NOT EXISTS winners (seasons number,winners_nation text,winners_team text,score number,'
    'runners_up_nation text,runners_up_team text,venue text,attendance number)')
conn.commit()

country_dict = {"ESP": "Spain", "ENG": "England", "ITA": "Italy", "GER": "Germany", "POR": "Portugal",
                "FRA": "France", "NED": "Netherlands", "POL": "Poland", "ROU": "Romania", "RUS": "Russia",
                "AUT": "Austria", "SCO": "Scotland", "SRB": "Serbia", "SUI": "Switzerland", "SVK": "Slovakia",
                "SVN": "SLovenia", "TUR": "Turkey", "NOR": "Norway", "ISR": "Israel", "KAZ": "Kazakhstan",
                "AZE": "Azerbaijan", "HUN": "Hungary", "GRE": "Greece", "FIN": "Finland", "DEN": "Denmark",
                "SWE": "Swedend", "CZE": "Czech Republic", "CYP": "Cyprus", "CRO": "Croatia", "BUL": "Bulgaria",
                "BLR": "Belarus", "BEL": "Belguim", "UKR": "Ukraine", "MDA": "Moldova", "IRL": "Ireland",
                "ALB": "Albania", "MLT": "Malta", "LVA": "Latvia", "NIR": "Northern Ireland", "LTU": "Lithuania",
                "GEO": "Georgia", "ISL": "Iceland", "ARM": "Armenia", "BIH": "Bosnia and Herzegovina",
                "LUX": "Luxemborg", "MKD": "North Macedonia", "EST": "Estonia", "WAL": "Wales", "FRO": "Faroe Island",
                "MNE": "Montegro", "KOS": "Kosovo", "GIB": "Gibraltar", "AND": "Andorra", "SMR": "San Marino"}

appearances_df = pd.read_csv('https://raw.githubusercontent.com/ZubairShaik7/NLP_Portfolio/main/PlayerAppearTotals.csv',
                             index_col='Unnamed: 0', sep=",")

goals_df = pd.read_csv('https://raw.githubusercontent.com/ZubairShaik7/NLP_Portfolio/main/PlayerGoalTotals.csv',
                       index_col='Unnamed: 0', sep=",")

clubs_df = pd.read_csv('https://raw.githubusercontent.com/ZubairShaik7/NLP_Portfolio/main/AllTimeRankingByClub.csv',
                       encoding="utf-16", sep=",")

winners_by_season_df = pd.read_csv(
    'https://raw.githubusercontent.com/ZubairShaik7/NLP_Portfolio/main/UCL%20History.csv', sep=",")

players_df = pd.read_csv('https://raw.githubusercontent.com/ZubairShaik7/NLP_Portfolio/main/FullData.csv', sep=",")

players_df.drop(
    columns=["National_Kit", "Club_Position", "Club_Kit", "Club_Joining", "Contract_Expiry", "Long_Shots", "Curve",
             "Freekick_Accuracy",
             "Penalties", "Volleys", "GK_Positioning", "GK_Diving", "GK_Kicking", "GK_Handling", "GK_Reflexes",
             "Acceleration", "Speed", "Stamina", "Strength", "Balance", "Agility", "Jumping",
             "Heading", "Shot_Power", "Finishing", "Standing_Tackle", "Aggression", "Reactions", "Attacking_Position",
             "Interceptions", "Vision", "Composure", "Crossing", "Short_Pass", "Long_Pass",
             "National_Position", "Work_Rate", "Weak_foot", "Skill_Moves", "Ball_Control", "Dribbling",
             "Marking", "Sliding_Tackle"], inplace=True)

players_df = players_df.rename(columns={'Name': 'Player'})

winners_by_season_df = winners_by_season_df.dropna()

print(clubs_df)

appearances_df['Appearances'] = appearances_df['Appearances'].astype(object)

goals_and_apps_df = pd.merge(goals_df, appearances_df, how='left')

players_combined_df = pd.merge(goals_and_apps_df, players_df, how='left')

# players_combined_df = players_combined_df.dropna()

print(players_combined_df)

print(winners_by_season_df)

clubs_df.to_sql('clubs', conn, if_exists='replace', index=False)

players_combined_df.to_sql('players', conn, if_exists='replace', index=False)

winners_by_season_df.to_sql('winners', conn, if_exists='replace', index=False)

c.close()
