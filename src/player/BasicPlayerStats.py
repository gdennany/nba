import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo, leaguedashplayerstats
from nba_api.stats.static import players

"""
Basic Player stats.
"""

def getActivePlayers():
    return players.get_active_players()

def getActivePlayerIDs():
    activePlayers = getActivePlayers()
    return [item['id'] for item in activePlayers]

def getPlayerByFullName(name):
    return players.find_players_by_full_name(name)

def getPlayerInfo(playerName):
    playerInfo = commonplayerinfo.CommonPlayerInfo(player_id=2544, timeout=100).get_data_frames()[0]
    return playerInfo

def getPlayerIdFromName(playerName):
    return getPlayerByFullName(playerName)[0]['id']

# Get stats for each active player in the NBA
# 
# Stats Returned:      PLAYER_ID,PLAYER_NAME,NICKNAME,TEAM_ID,TEAM_ABBREVIATION,AGE,GP,W,L,W_PCT,MIN,FGM,FGA,FG_PCT,FG3M,FG3A,FG3_PCT,FTM,FTA,FT_PCT,
#                      OREB,DREB,REB,AST,TOV,STL,BLK,BLKA,PF,PFD,PTS,PLUS_MINUS,NBA_FANTASY_PTS,DD2,TD3,GP_RANK,W_RANK,L_RANK,W_PCT_RANK,MIN_RANK,FGM_RANK,
#                      FGA_RANK,FG_PCT_RANK,FG3M_RANK,FG3A_RANK,FG3_PCT_RANK,FTM_RANK,FTA_RANK,FT_PCT_RANK,OREB_RANK,DREB_RANK,REB_RANK,AST_RANK,TOV_RANK,STL_RANK,
#                      BLK_RANK,BLKA_RANK,PF_RANK,PFD_RANK,PTS_RANK,PLUS_MINUS_RANK,NBA_FANTASY_PTS_RANK,DD2_RANK,TD3_RANK,CFID,CFPARAMS
#
# N=0 => get season averages for the above stats
# N=1 => get last game stats (technically is the average of the last game)
# N=5 => get average stats over last 5 games
def getBasicPlayerStats(N=0):
    return leaguedashplayerstats.LeagueDashPlayerStats(
      last_n_games=N,
      measure_type_detailed_defense='Base',
      month=0,
      opponent_team_id=0,
      pace_adjust='N',
      per_mode_detailed='PerGame',
      period=0,
      plus_minus='N',
      rank='N',
      season_type_all_star='Regular Season').get_data_frames()[0]

def testAdvanced(N=0):
    return leaguedashplayerstats.LeagueDashPlayerStats(
      last_n_games=N,
      measure_type_detailed_defense='Advanced',
      month=0,
      opponent_team_id=0,
      pace_adjust='N',
      per_mode_detailed='PerGame',
      period=0,
      plus_minus='N',
      rank='N',
      season_type_all_star='Regular Season').get_data_frames()[0]

# Gets the BasicPlayerStats for player specified by the players name. N convention is same as above.
def getPlayerStatsByName(playerName, N=0):
    playerID = getPlayerIdFromName(playerName)
    allPlayers = getBasicPlayerStats()
    return allPlayers.query('PLAYER_ID == @playerID')

def getPlayerStatsByID(playerID, N=0):
    allPlayers = getBasicPlayerStats()
    return allPlayers.query('PLAYER_ID == @playerID')


# Gets stat leader based on stat abbreviation (possible parameters listed in the "Stats Returned section above"). N convention is same as above.
def getStatLeader(statAbbreviation, N=0):
    return getBasicPlayerStats(N).sort_values(by=[statAbbreviation], ascending=False)[['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', statAbbreviation]]
