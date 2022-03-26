import pandas as pd
import src.player.AdvancedPlayerStats as AdvancedPlayerStats

def combineDataFrames():
    df = AdvancedPlayerStats.getFantasyPoints().sort_values(by=['PLAYER_ID'], ascending=False)
    
    usg = AdvancedPlayerStats.getPlayerUsagePCT().sort_values(by=['PLAYER_ID'], ascending=False)
    df['USG_PCT'] = usg['USG_PCT']

    hustle = AdvancedPlayerStats.getHustleStats().sort_values(by=['PLAYER_ID'], ascending=False)
    df['HUSTLE_POINTS'] = hustle['HUSTLE_POINTS']

    return df
