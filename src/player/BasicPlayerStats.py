import pandas as pd
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mappings
from nba_api.stats.endpoints import commonplayerinfo, leaguedashplayerstats
from nba_api.stats.static import players

"""
Basic Player stats.
"""

def getActivePlayers():
    return players.get_active_players()

def getPlayerByFullName(name):
    return players.find_players_by_full_name(name)

def getPlayerInfo(playerName):
    playerInfo = commonplayerinfo.CommonPlayerInfo(player_id=2544, timeout=100).get_data_frames()[0]
    return playerInfo

def getPlayerIdFromName(playerName):
    return getPlayerByFullName(playerName)[0]['id']

def getAllPlayerStats():
    #teamId = mappings.getTeamIdFromNickName(teamNickName)
    return leaguedashplayerstats.LeagueDashPlayerStats(
      last_n_games=0,
      measure_type_detailed_defense='Base',
      month=0,
      opponent_team_id=0,
      pace_adjust='N',
      per_mode_detailed='PerGame',
      period=0,
      plus_minus='N',
      rank='N',
      season_type_all_star='Regular Season').get_data_frames()[0]

def getPlayerStatsByName(playerName):
    playerId = getPlayerIdFromName(playerName)
    allPlayers = getAllPlayerStats()
    return allPlayers.query('PLAYER_ID == @playerId')

# Possible Parameters
def getStatLeader(statAbbreviation):
    return getAllPlayerStats().sort_values(by=[statAbbreviation], ascending=False)

def getAssistsLeaders():
    return getAllPlayerStats().sort_values(by=['AST'], ascending=False)

