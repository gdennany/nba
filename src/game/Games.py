import time
import pandas as pd
import src.team.BasicTeamStats as BasicTeamStats
from nba_api.stats.endpoints import leaguegamefinder, teamgamelog
from nba_api.stats.static import teams

def getAllGameIDs():
    gameIDs = []
    teamIDs = BasicTeamStats.getTeamIDs()

    #get game id for each game each team has played
    #print(BasicTeamStats.getGameIDsFromCurrentSeason(teamIDs[2]))

    for id in teamIDs:
        print(id)
        currentTeamsGamesList = teamgamelog.TeamGameLog(season='2021-22', season_type_all_star='Regular Season', team_id=id).get_data_frames()[0]['Game_ID'].values.tolist()
        for gameID in currentTeamsGamesList:
            if gameID not in gameIDs:
                gameIDs.append(gameID)

    #remove duplicates from list
    return gameIDs
