import pandas as pd
import src.player.AdvancedPlayerStats as AdvancedPlayerStats
import src.player.BasicPlayerStats as BasicPlayerStats
import src.player.ESPNAdvanced as RPM
import src.player.ESPNHollinger as PER

def combineDataFrames():
    # Get Fantasy Points and set as base dataframe
    df = AdvancedPlayerStats.getFantasyPoints().sort_values(by=['PLAYER_ID'], ascending=False)
    
    # Get Usage Percentage and combine to base dataframe
    usg = AdvancedPlayerStats.getPlayerUsagePCT().sort_values(by=['PLAYER_ID'], ascending=False)
    df['USG_PCT'] = usg['USG_PCT']

    # Get Hustle Stat Points and combine to base dataframe
    hustle = AdvancedPlayerStats.getHustleStats().sort_values(by=['PLAYER_ID'], ascending=False)
    df['HUSTLE_POINTS'] = hustle['HUSTLE_POINTS']
    
    # Get RPM data, match player names to playerID's, clean data, and combine to base dataframe
    rpm = RPM.get_rpm(2022)
    rpm['PLAYER_ID'] = rpm.apply(lambda row: df.loc[df['PLAYER_NAME'] == row.NAME][['PLAYER_ID']], axis=1)
    rpm['PLAYER_ID'] = rpm['PLAYER_ID'].astype(str)
    rpm['PLAYER_ID'] = rpm['PLAYER_ID'].str.split('\n').str[1]
    rpm['PLAYER_ID'] = rpm['PLAYER_ID'].str.split('    ').str[1]
    rpm['PLAYER_ID'] = rpm.apply(lambda row: row.PLAYER_ID.strip(), axis=1)
    rpm['PLAYER_ID'] = rpm['PLAYER_ID'].astype(int)
    rpm = rpm.sort_values(by=['PLAYER_ID'], ascending=False)
    df = df.reset_index(drop=True)
    rpm = rpm.reset_index(drop=True)
    #df['ORPM'] = rpm['ORPM']
    #df['DRPM'] = rpm['DRPM']
    df['RPM'] = rpm['RPM']
    df['WINS'] = rpm['WINS']
    #df['ID_MATCH'] = df.apply(lambda row: str(row.PLAYER_ID).strip() == str(row.WINS).strip(), axis=1)
    
    # Get PER data, match player names to playerID's, clean data, and combine to base dataframe
    per = PER.getPER()
    per['PLAYER_ID'] = per.apply(lambda row: df.loc[df['PLAYER_NAME'] == row.PLAYER][['PLAYER_ID']], axis=1)
    per['PLAYER_ID'] = per['PLAYER_ID'].astype(str)
    per['PLAYER_ID'] = per['PLAYER_ID'].str.split('\n').str[1]
    per['PLAYER_ID'] = per['PLAYER_ID'].str.split('    ').str[1]
    per['PLAYER_ID'] = per.apply(lambda row: row.PLAYER_ID.strip(), axis=1)
    per['PLAYER_ID'] = per['PLAYER_ID'].astype(int)
    per = per.sort_values(by=['PLAYER_ID'], ascending=False)
    per = per.drop_duplicates(subset=['PLAYER_ID'])
    df = df.reset_index(drop=True)
    per = per.reset_index(drop=True)
    df['PER'] = per['PER']
    
    # Check to ensure all PLAYER_ID's are matched up in the combined DF properly
    #df['ID_MATCH'] = df.apply(lambda row: str(row.PLAYER_ID).strip() == str(row.PER).strip(), axis=1)

    # Get career total stats
    careerStats = AdvancedPlayerStats.getPlayerCareerTotals_Sum().sort_values(by=['PLAYER_ID'], ascending=False)
    df['CAREER_PTS'] = careerStats['PTS']
    df['CAREER_AST'] = careerStats['AST']
    df['CAREER_REB'] = careerStats['REB']
    df['CAREER_STL'] = careerStats['STL']
    df['CAREER_BLK'] = careerStats['BLK']
    df['CAREER_TOV'] = careerStats['TOV']
    
    # TODO: add achievements (MVP, playoff appearances, etc) & factor in teams performance
    
    return df
