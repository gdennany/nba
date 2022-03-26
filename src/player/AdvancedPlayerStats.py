import matplotlib.pyplot as plot
import pandas as pd
import src.team.BasicTeamStats as BasicTeamStats
import src.player.BasicPlayerStats as BasicPlayerStats
import src.game.Games as Games
import mappings
from nba_api.stats.endpoints import leaguedashptstats, playerawards, leaguedashplayerbiostats, boxscoreplayertrackv2, leaguedashplayerstats, playercareerstats, teamplayerdashboard, leaguehustlestatsplayer

'''
Advanced Player Stats
'''
# Hustle Stats: https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguehustlestatsplayer.md

# many players who've played in a couple games this season are anomalies and need to be filtered
MIN_GAMES_PLAYED = 20
STEPH_CURRY_PLAYERID = 201939

def getAdvancedPlayerStats(N=0):
    df = leaguedashplayerstats.LeagueDashPlayerStats(
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
    
    return df.loc[df['GP'] > MIN_GAMES_PLAYED]

# Official NBA fantasy points ranking: 1 point scored => 1 point, 1 rebound => 1.2 points, 1 assist => 1.5 points, 1 blocked shot => 2 points 
#                                      1 steal => 2 points, 1 Turnover => -1 point
# This metric is especially useful because it awards players who play in a lot of games, and players who sit out often often don't have the chance
# to accumulate as many points. As well as players who are injured will slowly fall behind here
def getFantasyPoints():
    df = BasicPlayerStats.getBasicPlayerStatTotals()
    df = df[['PLAYER_ID', 'PLAYER_NAME', 'GP', 'NBA_FANTASY_PTS']]
    df = df.loc[df['GP'] > MIN_GAMES_PLAYED]
    df['AVG_FANTASY_PTS'] = round(df.apply(lambda row: row.NBA_FANTASY_PTS / row.GP, axis=1), 2)
    return df.sort_values(by=['NBA_FANTASY_PTS'], ascending=False)

# Usage Percentage => what percentatge of a team plays a player was involved in while he was on the court.
def getPlayerUsagePCT():
    playerStats = leaguedashplayerbiostats.LeagueDashPlayerBioStats(season='2021-22').get_data_frames()[0]
    playerStats = playerStats.loc[playerStats['GP'] > MIN_GAMES_PLAYED]
    '''
    playerStats.plot(kind='scatter',x='GP',y='USG_PCT')
    for idx, row in playerStats.iterrows():
        plot.annotate(row['PLAYER_NAME'], (row['GP'], row['USG_PCT']) )
    plot.show()
    '''
    return playerStats.sort_values(by=['USG_PCT'], ascending=False)[['PLAYER_ID', 'PLAYER_NAME', 'GP', 'USG_PCT']]

# Pace Factor, the number of possessions a team has per game (48 minutes), while a player is in the game
def getPACE():
    playerStats = getAdvancedPlayerStats()
    playerStats = playerStats.loc[playerStats['GP'] > MIN_GAMES_PLAYED]
    statName = 'PACE'
    return playerStats.sort_values(by=[statName], ascending=False)[['PLAYER_ID', 'PLAYER_NAME', 'GP', statName]]

def getPlayerNetRatings():
    playerStats = leaguedashplayerbiostats.LeagueDashPlayerBioStats(season='2021-22').get_data_frames()[0]
    playerStats = playerStats.loc[playerStats['GP'] > MIN_GAMES_PLAYED]
    #statName = 'NET_RATING'
    return playerStats
    #return playerStats.sort_values(by=[statName], ascending=False)[['PLAYER_ID', 'PLAYER_NAME', 'GP', statName]]

# getPlayerCareer... methods below all use: https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playercareerstats.md
def getPlayerCareerAverages():
    df = leaguedashptstats.LeagueDashPtStats(
        player_or_team = 'Player',
        last_n_games=0,
        month=0,
        opponent_team_id=0,
        season_type_all_star='Regular Season').get_data_frames()[0]
    return df

def getPlayerCareerTotals_BySeason(playerID=STEPH_CURRY_PLAYERID):
    activePlayerIDs = BasicPlayerStats.getActivePlayerIDs()
    return playercareerstats.PlayerCareerStats(per_mode36='Totals', player_id=STEPH_CURRY_PLAYERID).get_data_frames()[0]
    #for id in activePlayerIDs:

def getPlayerCareerTotals_Sum(playerID=STEPH_CURRY_PLAYERID):
    activePlayerIDs = BasicPlayerStats.getActivePlayerIDs()
    df = playercareerstats.PlayerCareerStats(per_mode36='Totals', player_id=STEPH_CURRY_PLAYERID).get_data_frames()[0]
    return df.groupby("PLAYER_ID").sum()

def getPlayerCareerAverages_BySeason(playerID=STEPH_CURRY_PLAYERID):
    activePlayerIDs = BasicPlayerStats.getActivePlayerIDs()
    return playercareerstats.PlayerCareerStats(per_mode36='PerGame', player_id=STEPH_CURRY_PLAYERID).get_data_frames()[0]
    #for id in activePlayerIDs:

def getPlayerCareerAverages(playerID=STEPH_CURRY_PLAYERID):
    df = playercareerstats.PlayerCareerStats(per_mode36='PerGame', player_id=STEPH_CURRY_PLAYERID).get_data_frames()[0]
    seasonsPlayed = df.shape[0]
    df = df.groupby("PLAYER_ID").sum()
    df = round(df.apply(lambda row: row / seasonsPlayed, axis=1), 2)
    return df

# https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/leaguehustlestatsplayer.md
# 1 contested shot => 0.8 points, 1 deflection => 4 points, 1 charge drawn => 10 points, 1 screen assist point (screen for someone who then scores) => 0.8 points, 1 loose ball recoverd => 2 points
# contested shot => big man favored stat (max rn: 871)
# screen assist points => big man favored stat (max rn: 919)
# deflections => gaurd favored stat (max rn: 256)
# loose balls recovered => mainly gaurd favored state (max rn: 74)
# charges drawn => mix (max rn: 25)
# tried to make wieghts such that: big man favored stats hold ~1/2 weight that gaurd favored stats do. This data is heavily skewed to favore big men
def getHustleStats():
    df = leaguehustlestatsplayer.LeagueHustleStatsPlayer(per_mode_time='Totals', season_type_all_star='Regular Season').get_data_frames()[0]
    df = df.loc[df['G'] > MIN_GAMES_PLAYED]
    df = df[['PLAYER_ID', 'PLAYER_NAME', 'G', 'CONTESTED_SHOTS', 'DEFLECTIONS', 'CHARGES_DRAWN', 'SCREEN_AST_PTS', 'LOOSE_BALLS_RECOVERED']]
    df['HUSTLE_POINTS'] = round(df.apply(lambda row: (row.CONTESTED_SHOTS * 0.57) + (row.DEFLECTIONS * 3.9) + (row.CHARGES_DRAWN * 10) + (row.SCREEN_AST_PTS * 0.54) + (row.LOOSE_BALLS_RECOVERED * 13.5), axis=1), 2)
    return df.sort_values(by=['HUSTLE_POINTS'], ascending=False)

'''
# John Hollinger's Player Efficiency Rating (PER) is a one-number measure of a player's per-minute productivity
# unfortunately is just an estimation of actual http://insider.espn.com/nba/hollinger/statistics
def getPlayerEfficiencyRating():
    df = BasicPlayerStats.getBasicPlayerStatTotals()
    df = df[['PLAYER_ID', 'PLAYER_NAME', 'GP', 'FGA', 'FGM', 'STL', 'FG3M', 'FTA', 'FTM', 'BLK', 'OREB', 'AST', 'DREB', 'PF', 'TOV', 'MIN']]
    df = df.loc[df['GP'] > MIN_GAMES_PLAYED]
    df['FT_MISS'] = df.apply(lambda row: row.FTA - row.FTM, axis=1)
    df['FG_MISS'] = df.apply(lambda row: row.FGA - row.FGM, axis=1)
    df['PER'] = round(df.apply(lambda row: calculatePER(row), axis=1), 2)
    return df.sort_values(by=['PER'], ascending=False)[['PLAYER_ID', 'PLAYER_NAME', 'PER']]

# See here for more on calculating PER with these linear weights https://bleacherreport.com/articles/113144-cracking-the-code-how-to-calculate-hollingers-per-without-all-the-mess
def calculatePER(row):
    wFGM = row.FGM * 85.91
    wSTL = row.STL * 53.897
    wFG3M = row.FG3M * 51.757
    wFTM = row.FTM * 46.845
    wBLK = row.BLK * 39.190
    wOREB = row.OREB * 39.190
    wAST = row.AST * 34.677
    wDREB = row.DREB * 14.707
    wPF = row.PF * 17.174
    wFTMISS = row.FT_MISS * 20.091
    wFGMISS = row.FG_MISS * 39.190
    wTOV = row.TOV * 53.897

    positive = wFGM + wSTL + wFG3M + wFTM + wBLK + wOREB + wAST + wDREB
    negative = wPF + wFTMISS + wFGMISS + wTOV

    return (positive - negative) * (1 / row.MIN)

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
    #SAST => https://github.com/swar/nba_api/blob/7f0c1dacf46c9fc2112b975be77e08666cb5934e/docs/nba_api/stats/endpoints/boxscoreplayertrackv2.md or
    #        https://github.com/swar/nba_api/blob/7f0c1dacf46c9fc2112b975be77e08666cb5934e/docs/nba_api/stats/endpoints/leaguehustlestatsplayer.md
    #FTAST => cant get
    #OPAST => https://github.com/swar/nba_api/blob/7f0c1dacf46c9fc2112b975be77e08666cb5934e/docs/nba_api/stats/endpoints/leaguehustlestatsplayer.md
    #PACE => getPACE()

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
    
def test():
    return playerawards.PlayerAwards(player_id=STEPH_CURRY_PLAYERID).get_data_frames()[0]


# https://fivetimesfive-blog.com/2017/05/28/direct-offensive-contribution-doc/
def getDirectOffensiveContribution():
    pass

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

def getFantasyPoints():
    ls = []
    activePlayers = BasicPlayerStats.getActivePlayers()  
    print('start')
    for i in range(1, 15):
        player = activePlayers[randrange(0, len(activePlayers))]
        cur = playerfantasyprofile.PlayerFantasyProfile(season='2021-22', player_id = player['id']).get_data_frames()[0][['NBA_FANTASY_PTS']]
        try:
            bio = [player['id'], player['full_name'], int(cur.iat[0,0])]
            ls.append(bio)
            print(bio)
        except:
            pass    
    return pd.DataFrame(ls, columns=['PLAYER_ID', 'FULL_NAME', 'FANTASY_POINTS']).sort_values(by=['FANTASY_POINTS'], ascending=False)
'''

