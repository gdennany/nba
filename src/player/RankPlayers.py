import pandas as pd
import src.player.AdvancedPlayerStats as AdvancedPlayerStats
import src.player.BasicPlayerStats as BasicPlayerStats
import src.player.ESPNAdvanced as RPM
from nba_api.stats.endpoints.commonallplayers import CommonAllPlayers

def combineDataFrames():
    df = AdvancedPlayerStats.getFantasyPoints().sort_values(by=['PLAYER_ID'], ascending=False)
    
    usg = AdvancedPlayerStats.getPlayerUsagePCT().sort_values(by=['PLAYER_ID'], ascending=False)
    df['USG_PCT'] = usg['USG_PCT']

    hustle = AdvancedPlayerStats.getHustleStats().sort_values(by=['PLAYER_ID'], ascending=False)
    df['HUSTLE_POINTS'] = hustle['HUSTLE_POINTS']
    
    rpm = RPM.get_rpm(2022)
    rpm['PLAYER_ID'] = rpm.apply(lambda row: df.loc[df['PLAYER_NAME'] == row.NAME][['PLAYER_ID']], axis=1)
    #rpm['PLAYER_ID'] = rpm.apply(lambda row: BasicPlayerStats.getPlayerByFullName(row.NAME)[0], axis=1)
    #all_players = CommonAllPlayers(is_only_current_season=1).get_dict()
    #print(all_players)
    rpm['PLAYER_ID'] = rpm['PLAYER_ID'].astype(str)

    rpm['PLAYER_ID'] = rpm['PLAYER_ID'].str.split('\n').str[1]
    rpm['PLAYER_ID'] = rpm['PLAYER_ID'].str.split('    ').str[1]
    rpm['PLAYER_ID'] = rpm.apply(lambda row: row.PLAYER_ID.strip(), axis=1)
    #rpm.to_numeric(totalDF['GP'])
    return rpm
