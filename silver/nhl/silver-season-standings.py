# %%
import json
import os

# %%

def formatRawToSilver(data, team_info, stat_groups, filename):
    season_data = data['standings']
    formatted_season_data = []
    
    for team in season_data:

        stats_obj = {}
        for group, keys in stat_groups.items():
            stats_obj[group] = {}
            for key in keys:
                if key in team:
                    stats_obj[group][key] = team[key]

        team_obj = {}
        for group, keys in team_info.items():
            team_obj[group] = {}
            for key in keys:
                if key in team:
                    team_obj[group][key] = team[key]

        team_obj["statistics"] = stats_obj
        formatted_season_data.append(team_obj)

    season_obj = {}
    season_obj['season_identifier'] = f'{filename[4:8]}'   # return '2008' for '20072008.json'
    season_obj['full_season_identifier'] = f'{filename[0:4]}-{filename[4:8]}'  # return '2007-2008' for '20072008.json'
    season_obj['season_game_type'] = 'Regular Season'
    season_obj['season_data'] = formatted_season_data
    
    return season_obj

#%%


# open local json files from raw standings folder
data_path = "../../raw/nhl/data/standings/"
files = [file for file in os.listdir(data_path)]


#%%
team_info = {
        "team":["teamCommonName", "teamAbbrev", "teamName", "placeName", "conferenceName", "divisionAbbrev", "conferenceAbbrev"]
    }

stat_groups = {
    "game_stats": ["gamesPlayed", "homeGamesPlayed", "roadGamesPlayed"],
    "goals_stats": ["goalDifferential", "goalDifferentialPctg", "goalAgainst", "goalFor", "goalsForPctg", "homeGoalDifferential", "homeGoalsAgainst", "homeGoalsFor", "roadGoalDifferential", "roadGoalsAgainst", "roadGoalsFor"],
    "wins_and_losses": ["wins", "losses", "regulationWins", "otLosses", "shootoutWins", "shootoutLosses", "homeWins", "homeLosses", "homeTies", "homeRegulationWins", "homeRegulationPlusOtWins", "homeOtLosses", "roadWins", "roadLosses", "roadOtLosses", "roadTies", "roadRegulationWins", "roadRegulationPlusOtWins", "ties", "winPctg", "regulationWinPctg", "regulationPlusOtWins", "regulationPlusOtWinPctg"],
    "points":["points", "homePoints", "roadPoints", "regulationPlusOtWinPctg", "pointPctg"]
}

#%% 

for file in files:
    with open(os.path.join(data_path, file), "r") as json_file:
        data = json.load(json_file)
        silver_data = formatRawToSilver(data, team_info, stat_groups, file)

        filename = os.path.join(os.path.dirname(__file__), "data", "standings", file)
        with open(filename, "w") as silver_file:
            json.dump(silver_data, silver_file)