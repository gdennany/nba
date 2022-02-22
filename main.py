import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import src.player.BasicPlayerStats as BasicPlayerStats
import src.player.AdvancedPlayerStats as AdvancedPlayerStats
import src.team.BasicTeamStats as BasicTeamStats
import src.game.Games as Games

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
    #AdvancedPlayerStats.getAdvancedStatAveragesByTeam("Pacers").to_csv('out.csv')
    #AdvancedPlayerStats.getInvolveMentRate()
    #Games.getAllGameIDs()
    AdvancedPlayerStats.getFantasyPoints().to_csv('out.csv')
    #Games.test().to_csv('out.csv')

def toCSV(dataframe):
    dataframe.to_csv('out.csv')

if __name__ == "__main__":
    main()

    