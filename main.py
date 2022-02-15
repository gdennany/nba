import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import src.player.BasicPlayerStats as BasicPlayerStats
import src.team.BasicTeamStats as BasicTeamStats

def main():
    '''
    team_df = pd.DataFrame(teams.get_teams())

    team_df[team_df['nickname'] == 'Knicks']

    knicks_42 = leaguegamefinder.LeagueGameFinder(season_nullable='2020-21', team_id_nullable='1610612752', league_id_nullable='00', season_type_nullable='Regular Season').get_data_frames()[0][:42]

    knicks_42['PTS'].mean()
    print(knicks_42['PTS'].mean())
    '''
    #print(BasicPlayerStats.getSeasonStats())

    #print(BasicTeamStats.getTeamByNickname("Celtics"))
    #print(BasicTeamStats.getTeamRosterStats("Knicks"))
    #print(BasicTeamStats.getRecentGames("Pacers"))
    
    #players = BasicPlayerStats.getActivePlayers()
    #for player in players:
    #    print(player)

    #print(BasicPlayerStats.getPlayerInfo("Myles Turner"))
    #print(BasicPlayerStats.getPlayerByFullName("Myles Turner"))
    #print(BasicPlayerStats.getPlayerStatsByName("RJ Barret"))
    #print(BasicPlayerStats.getAllPlayerStats().to_csv('out'))
    #print(BasicPlayerStats.getPlayerStatsByName("Ja Morant"))
    print(BasicPlayerStats.getStatLeader("FG3M_RANK"))
    #print(BasicPlayerStats.getAssistsLeaders().to_csv('out'))

if __name__ == "__main__":
    main()

    