from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import src.player.BasicPlayerStats as BasicPlayerStats

MIN_GAMES_PLAYED = 20
# Real Plus Minus: https://www.nbastuffer.com/analytics101/real-plus-minus-rpm/
def get_rpm(year):
    totalDF = pd.DataFrame()
    for j in range(14):
        if(j == 0):
            url = "http://www.espn.com/nba/statistics/rpm/_/year/{}".format(year)
            html = urlopen(url)
            soup = BeautifulSoup(html, features="html.parser")
            soup.findAll('tr', limit=2)
            headers = [td.getText() for td in soup.findAll('tr', limit=2)[0].findAll('td')]
            rows = soup.findAll('tr')[1:]
            player_stats = [[td.getText() for td in rows[year].findAll('td')]
                for year in range(len(rows))]

            df = pd.DataFrame(player_stats, columns = headers)
            df.set_index("RK")
            totalDF = pd.concat([totalDF, df])
        else:
            url = "http://www.espn.com/nba/statistics/rpm/_/year/{}/page/{}".format(year, j+1)
            html = urlopen(url)
            soup = BeautifulSoup(html, features="html.parser")
            soup.findAll('tr', limit=2)
            headers = [td.getText() for td in soup.findAll('tr', limit=2)[0].findAll('td')]
            rows = soup.findAll('tr')[1:]
            player_stats = [[td.getText() for td in rows[year].findAll('td')]
                for year in range(len(rows))]

            df = pd.DataFrame(player_stats, columns = headers)
            df.set_index("RK")
            totalDF = pd.concat([totalDF, df])

    # Convert GP column to int
    totalDF['GP'] = pd.to_numeric(totalDF['GP'])

    # Filter out players who've played < MIN_GAMES_PLAYED (20 as of now) games
    totalDF = totalDF.loc[totalDF['GP'] > MIN_GAMES_PLAYED]

    # Remove team abbreviation after player name
    totalDF['NAME'] = totalDF['NAME'].str.split(',').str[0]
    
    totalDF = totalDF[['NAME', 'ORPM', 'DRPM', 'RPM', 'WINS']]
    
    return totalDF
        
        
