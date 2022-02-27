import pandas as pd
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mappings
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder, leaguedashplayerstats, franchisehistory,leaguestandings

CURRENT_SEASON_ID = '22021'

# League Standings => https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguestandings.md
def getTeams():
    return teams.get_teams()

def getTeamIDs():
    teamIDs = []
    teams = getTeams()
    for team in teams:
        teamIDs.append(team['id'])
    return teamIDs

def getTeamByNickname(teamNickname):
    teams = getTeams()
    for team in teams:
        if (team.get("nickname") == teamNickname):
            return team

def getTeamNameByID(teamID):
    teams = getTeams()
    for team in teams:
        if (team.get('id') == teamID):
            return team.get('full_name')

# API: https://github.com/swar/nba_api/blob/7f0c1dacf46c9fc2112b975be77e08666cb5934e/docs/nba_api/stats/endpoints/leaguegamefinder.md
# For each game this season (for the input team), return "LeagueGameFinderResults" from above api link
def getTeamGamesThisSeason(teamID):
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=teamID, season_nullable='2021-22')
    games = gamefinder.get_data_frames()[0]
    return games
'''
def getTeamGamesThisSeason(teamNickname):
    teamId = getTeamByNickname(teamNickname).get('id')
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=teamId, season_nullable='2021-22')
    games = gamefinder.get_data_frames()[0]
    return games
'''

# Returns each gameID this team has played in this season
def getGameIDsFromCurrentSeason(teamID):
    return getTeamGamesThisSeason(teamID)[['GAME_ID']]
    
def getTeamAverageStatsByPlayer(teamNickName, N=0):
    teamId = mappings.getTeamNickNameToIDMapping(teamNickName)
    return leaguedashplayerstats.LeagueDashPlayerStats(
      team_id_nullable=teamId,
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

def getTeamAverageAdvancedStatsByPlayer(teamNickName, N=0):
    teamId = mappings.getTeamNickNameToIDMapping(teamNickName)
    return leaguedashplayerstats.LeagueDashPlayerStats(
      team_id_nullable=teamId,
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

def getTeamStatLeaders(teamNickname, statAbbreviation, N=0):
    teamStats = getTeamAverageStatsByPlayer(teamNickname, N)
    return teamStats.sort_values(by=[statAbbreviation], ascending=False)[['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ABBREVIATION', statAbbreviation]]

# https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/franchisehistory.md
def getFranchiseHistory():
    df = franchisehistory.FranchiseHistory().get_data_frames()[0]
    keys = df.groupby("TEAM_ID").groups.keys()
    df = df.groupby("TEAM_ID").sum()
    df['TEAM_ID'] = keys
    df = df[['TEAM_ID', 'PO_APPEARANCES', 'DIV_TITLES', 'CONF_TITLES', 'LEAGUE_TITLES']]
    df['TEAM_NAME'] = df.apply(lambda row: getTeamNameByID(row.TEAM_ID), axis=1)
    df = df[['TEAM_ID', 'TEAM_NAME','PO_APPEARANCES', 'DIV_TITLES', 'CONF_TITLES', 'LEAGUE_TITLES']]
    return df

# many more attributes you could grab https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguestandings.md
def getLeagueStandiangs():
    df = leaguestandings.LeagueStandings().get_data_frames()[0]
    df = df[['TeamID', 'TeamName', 'Record', 'Conference', 'WINS', 'LOSSES', 'WinPCT', 'L10', 'CurrentStreak', 'PointsPG', 'OppPointsPG', 'DiffPointsPG']]
    return df.sort_values(by=['WinPCT'], ascending=False)
# Get result for teams last N games 
#def getTeamsLastNGames(teamNickName, n):


