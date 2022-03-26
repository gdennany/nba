import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import src.player.BasicPlayerStats as BasicPlayerStats
import src.player.AdvancedPlayerStats as AdvancedPlayerStats
import src.team.BasicTeamStats as BasicTeamStats
import src.game.Games as Games
import src.player.ESPNAdvanced as ESPN
import src.player.ESPNHollinger as Hollinger

# number of players with > 20 games played: 416
def main():
    #print(BasicPlayerStats.getActivePlayers())
    #print(BasicPlayerStats.getPlayerByFullName("Ja Morant"))
    #BasicPlayerStats.testAdvanced().to_csv('out.csv')
    #BasicPlayerStats.getPlayerStatsByName("Chris Paul").to_csv('out.csv')
    #BasicPlayerStats.getStatLeader("AST").to_csv('out.csv')
    #print(BasicTeamStats.getTeamsRecentGames("Lakers"))
    #BasicPlayerStats.getStatLeader("AST", 5).to_csv('out.csv')
    #BasicTeamStats.getTeamAverageStatsByPlayer("Lakers").to_csv('out.csv')
    #BasicTeamStats.getTeamsRecentGames("Lakers").to_csv('out.csv')
    #print(BasicTeamStats.getTeamLastNGameStatAveragesByPlayer("Lakers", 1))
    #BasicTeamStats.getTeamStatLeaders("Lakers", "AST", 1).to_csv('out.csv')
    #BasicTeamStats.getTeamStatLeaders()
    #print(BasicTeamStats.getTeamGamesThisSeason("Pacers"))
    #AdvancedPlayerStats.getAdvancedStatAveragesByTeam("Pacers").to_csv('out.csv')
    #AdvancedPlayerStats.getHustleStats().to_csv('out.csv')
    #AdvancedPlayerStats.getInvolveMentRate()
    #Games.getAllGameIDs()
    #BasicTeamStats.getLeagueStandiangs().to_csv('out.csv')
    #ESPN.get_rpm([2022]).to_csv('out.csv')
    #BasicPlayerStats.getBasicPlayerStatTotals().to_csv('out.csv')
    #Games.test().to_csv('out.csv')

    #AdvancedPlayerStats.getHustleStats().to_csv('out.csv')
    #ESPN.get_rpm([2022]).sort_values(by=['DRPM'], ascending=False).to_csv('out.csv')
    getPlayerProfile()
    #getTeamProfile()


def getPlayerProfile():
    #AdvancedPlayerStats.getFantasyPoints().to_csv('player_fantasyPoints.csv')
    Hollinger.getPER().to_csv('player_per.csv')
    #AdvancedPlayerStats.getPlayerUsagePCT().to_csv('player_usg.csv')
    #ESPN.get_rpm([2022]).to_csv('player_rpm.csv')
    #AdvancedPlayerStats.getAdvancedPlayerStats().to_csv('player_statsAdvanced.csv')
    #AdvancedPlayerStats.getPlayerCareerTotals_BySeason().to_csv('player_careerTotalsBySeason.csv')
    #AdvancedPlayerStats.getPlayerCareerTotals_Sum().to_csv('player_careerTotalsSum.csv')
    #AdvancedPlayerStats.getPlayerCareerAverages_BySeason().to_csv('player_averagesBySeason.csv')
    #AdvancedPlayerStats.getPlayerCareerAverages().to_csv('player_careerAverages.csv')
    #AdvancedPlayerStats.getPlayerNetRatings().to_csv('out.csv')
    #AdvancedPlayerStats.getHustleStats().to_csv('player_hustleStats.csv')
    pass

def getTeamProfile():
    BasicTeamStats.getLeagueStandiangs().to_csv('team_standings.csv')
    BasicTeamStats.getTeamAverageStatsByPlayer('Grizzlies').to_csv('team_playerStats.csv')
    BasicTeamStats.getFranchiseHistory().to_csv('team_history.csv')
    BasicTeamStats.getTeamAverageAdvancedStatsByPlayer("Lakers").to_csv('team_advancedPlayerStats.csv')

def toCSV(dataframe):
    dataframe.to_csv('out.csv')

if __name__ == "__main__":
    main()

    