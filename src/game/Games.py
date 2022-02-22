import time
import pandas as pd
import src.team.BasicTeamStats as BasicTeamStats
from nba_api.stats.endpoints import leaguegamefinder, teamgamelog, leaguegamelog, leaguedashptstats
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

def test():
    '''
    game_log = leaguegamelog.LeagueGameLog(player_or_team_abbreviation = 'P', season = '2021-22')
    df = game_log.league_game_log.get_data_frame()[0]
    return df
    '''
    player_distance = leaguedashptstats.LeagueDashPtStats(player_or_team = 'Player')
    df = player_distance.league_dash_pt_stats.get_data_frame()
    return df.loc[df['PLAYER_ID'] == 203932]
    
