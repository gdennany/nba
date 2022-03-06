from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import os

MIN_GAMES_PLAYED = 20
# TODO: filter out by min_games_played
# Real Plus Minus: https://www.nbastuffer.com/analytics101/real-plus-minus-rpm/
def get_rpm(years):
    totalDF = pd.DataFrame()
    for i in years:
        for j in range(14):
            if(j == 0):
                url = "http://www.espn.com/nba/statistics/rpm/_/year/{}".format(i)
                html = urlopen(url)
                soup = BeautifulSoup(html, features="html.parser")
                soup.findAll('tr', limit=2)
                headers = [td.getText() for td in soup.findAll('tr', limit=2)[0].findAll('td')]
                rows = soup.findAll('tr')[1:]
                player_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]

                df = pd.DataFrame(player_stats, columns = headers)
                df.set_index("RK")
                totalDF = pd.concat([totalDF, df])
            else:
                url = "http://www.espn.com/nba/statistics/rpm/_/year/{}/page/{}".format(i, j+1)
                html = urlopen(url)
                soup = BeautifulSoup(html, features="html.parser")
                soup.findAll('tr', limit=2)
                headers = [td.getText() for td in soup.findAll('tr', limit=2)[0].findAll('td')]
                rows = soup.findAll('tr')[1:]
                player_stats = [[td.getText() for td in rows[i].findAll('td')]
                    for i in range(len(rows))]

                df = pd.DataFrame(player_stats, columns = headers)
                df.set_index("RK")
                totalDF = pd.concat([totalDF, df])

        return totalDF
        
        
