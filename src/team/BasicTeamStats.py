import pandas as pd
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mappings
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder, leaguedashplayerstats

def getTeams():
    return teams.get_teams()

def getTeamByNickname(teamNickname):
    teams = getTeams()
    for team in teams:
        if (team.get("nickname") == teamNickname):
            return team

def getTeamsRecentGames(teamNickname):
    teamId = getTeam(teamNickname).get("id")
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=teamId)
    games = gamefinder.get_data_frames()[0]
    return games
    
def getTeamRosterStats(teamNickName):
    teamId = mappings.getTeamIdFromNickName(teamNickName)
    return leaguedashplayerstats.LeagueDashPlayerStats(
      team_id_nullable=teamId,
      last_n_games=0,
      measure_type_detailed_defense='Base',
      month=0,
      opponent_team_id=0,
      pace_adjust='N',
      per_mode_detailed='PerGame',
      period=0,
      plus_minus='Y',
      rank='Y',
      season_type_all_star='Regular Season').get_data_frames()[0]

