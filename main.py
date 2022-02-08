import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

def main():
    team_df = pd.DataFrame(teams.get_teams())

    team_df[team_df['nickname'] == 'Knicks']

    knicks_42 = leaguegamefinder.LeagueGameFinder(season_nullable='2020-21', team_id_nullable='1610612752',                               league_id_nullable='00', season_type_nullable='Regular Season').get_data_frames()[0][:42]

    knicks_42['PTS'].mean()
    print(knicks_42['PTS'].mean())
    print("Hello World!")

if __name__ == "__main__":
    main()