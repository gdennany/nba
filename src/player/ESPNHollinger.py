import pandas as pd

MIN_GAMES_PLAYED = 20

# John Hollinger's Player Efficiency Rating (PER) is a one-number measure of a player's per-minute productivity
def getPER():
    # Read PER data from https://insider.espn.com/nba/hollinger/statistics/_/qualified/false and convert to pandas dataframe
    fullDF = pd.read_html('https://insider.espn.com/nba/hollinger/statistics/_/qualified/false', header=1)[0]
    
    # There are multiple pages of data to read from, i.e. https://insider.espn.com/nba/hollinger/statistics/_/page/2/qualified/false is the third page of data we need to read
    try:
        # Read every page of data until there are no more pages to read (errors out and goes to except block)
        pageNum = 1
        while (True):
            # append this page of data to full dataframe
            url = f'https://insider.espn.com/nba/hollinger/statistics/_/page/{pageNum}/qualified/false'
            df = pd.read_html(url, header=1)[0]
            if not df.empty:
                fullDF = pd.concat([fullDF, df])
            else:
                raise pd.errors.EmptyDataError('No more pages to read')
            pageNum += 1
    except:
        pass 

    # Drop useless rows of data
    fullDF.drop(fullDF[fullDF['PLAYER'] == 'PLAYER'].index, inplace = True)

    # Convert GP column to int
    fullDF['GP'] = pd.to_numeric(fullDF['GP'])

    # Filter out players who've played < MIN_GAMES_PLAYED (20 as of now) games
    fullDF = fullDF.loc[fullDF['GP'] > MIN_GAMES_PLAYED]

    # Remove team abbreviation after player name
    fullDF['PLAYER'] = fullDF['PLAYER'].str.split(',').str[0]

    # Get only columns we we want
    fullDF = fullDF[['PLAYER', 'GP', 'PER']]

    return fullDF