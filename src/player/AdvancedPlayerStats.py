import pandas as pd
import src.team.BasicTeamStats as BasicTeamStats
import src.player.BasicPlayerStats as BasicPlayerStats
import src.game.Games as Games
import mappings
from nba_api.stats.endpoints import playerestimatedmetrics, boxscoreadvancedv2, leaguedashplayerbiostats, boxscoreplayertrackv2, leaguedashplayerstats

'''
Advanced Player Stats
'''

# many players who've played in a couple games this season are anomalies and need to be filtered
MIN_GAMES_PLAYED = 20
STEPH_CURRY_PLAYERID = 201939

def getAdvancedStatAveragesByTeam(teamNickName):
    #teamGamesThisSeason = BasicTeamStats.getGameIDsFromCurrentSeason(teamNickName)
    #return boxscoreadvancedv2.BoxScoreAdvancedV2(game_id = '0022100618').get_data_frames()[0]
    playerIDList = BasicPlayerStats.getActivePlayerIDs()

def getAdvancedPlayerStats(N=0):
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

# API used: https://github.com/swar/nba_api/blob/7f0c1dacf46c9fc2112b975be77e08666cb5934e/docs/nba_api/stats/endpoints/leaguedashplayerbiostats.md
def getPlayerUsageRates():
    playerStats = leaguedashplayerbiostats.LeagueDashPlayerBioStats(season='2021-22').get_data_frames()[0]
    playerStats = playerStats.loc[playerStats['GP'] > MIN_GAMES_PLAYED]
    statName = 'USG_PCT'
    return playerStats.sort_values(by=[statName], ascending=False)[['PLAYER_ID', 'PLAYER_NAME', 'GP', statName]]

def getPACE():
    playerStats = getAdvancedPlayerStats()
    playerStats = playerStats.loc[playerStats['GP'] > MIN_GAMES_PLAYED]
    statName = 'PACE'
    return playerStats.sort_values(by=[statName], ascending=False)[['PLAYER_ID', 'PLAYER_NAME', 'GP', statName]]

def getPlayerNetRatings():
    playerStats = leaguedashplayerbiostats.LeagueDashPlayerBioStats(season='2021-22').get_data_frames()[0]
    playerStats = playerStats.loc[playerStats['GP'] > MIN_GAMES_PLAYED]
    statName = 'NET_RATING'
    return playerStats.sort_values(by=[statName], ascending=False)[['PLAYER_ID', 'PLAYER_NAME', 'GP', statName]]

# https://fivetimesfive-blog.com/2017/05/22/new-statistics-involvement-rate/
def getInvolveMentRate():
    basicPlayerStats = BasicPlayerStats.getPlayerStatsByID(STEPH_CURRY_PLAYERID)

    FGA = basicPlayerStats['FGA']
    FTA = basicPlayerStats['FTA'] * 0.44
    AST = basicPlayerStats['AST']
    OREB = basicPlayerStats['OREB']
    TOV = basicPlayerStats['TOV']
    MP = basicPlayerStats['MIN']
    GP = basicPlayerStats['GP']
    TMP = 48
    #SAST => https://github.com/swar/nba_api/blob/7f0c1dacf46c9fc2112b975be77e08666cb5934e/docs/nba_api/stats/endpoints/boxscoreplayertrackv2.md
    #FTAST => cant get
    #OPAST => https://github.com/swar/nba_api/blob/7f0c1dacf46c9fc2112b975be77e08666cb5934e/docs/nba_api/stats/endpoints/leaguehustlestatsplayer.md
    #PACE => https://github.com/swar/nba_api/blob/7f0c1dacf46c9fc2112b975be77e08666cb5934e/docs/nba_api/stats/endpoints/boxscoreadvancedv2.md

    #testGameId = '0022100194'
    SASTDict = {}
    for game in mappings.gameIDs():
        print(game)
        boxScore = boxscoreplayertrackv2.BoxScorePlayerTrackV2(game).get_data_frames()[0]
        for score in boxScore[['PLAYER_ID', 'SAST']].values.tolist():
            playerID = score[0]
            if playerID not in SASTDict:
                SASTDict[score[0]] = score[1]
            else:
                total = SASTDict.get(score[0])
                SASTDict[score[0]] = total + score[1]
    


    #return boxscoreplayertrackv2.BoxScorePlayerTrackV2(testGameId).get_data_frames()[0]
    

    
    


# https://fivetimesfive-blog.com/2017/05/28/direct-offensive-contribution-doc/
def getDirectOffensiveContribution():
    pass

'''
The following methods rely on the "playerestimatedmetrics" (https://github.com/swar/nba_api/blob/7f0c1dacf46c9fc2112b975be77e08666cb5934e/docs/nba_api/stats/endpoints/playerestimatedmetrics.md).
 Not sure exactly what this data is so I decided against using it

def getPlayerMetrics():
    return playerestimatedmetrics.PlayerEstimatedMetrics(season='2021-22').get_data_frames()[0]


# Usage Rate: what percentatge of a team plays a player was involved in while he was on the court.
# https://www.nbastuffer.com/analytics101/usage-rate/
def getUsageRate():
    df = getPlayerMetrics()
    df = df.loc[df['GP'] > MIN_GAMES_PLAYED]
    return df.sort_values(by=['E_OFF_RATING'], ascending=False)[['PLAYER_ID', 'PLAYER_NAME', 'GP', 'E_OFF_RATING']]

# Net Rating; Offensive Rating minus Defensive Rating
# Example: for every 100 possessions played by the Warriors when Curry is on the floor, they scored an average of 119 points 
# and allowed 105 resulting in a net rating of ~14 for Curry.
# https://www.pivotanalysis.com/post/net-rating#:~:text=Net%20rating%20is%20the%20offensive,a%20per%20X%20possessions%20basis.
def getNetRating():
    pass
'''
