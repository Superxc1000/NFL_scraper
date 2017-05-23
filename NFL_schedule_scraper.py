from bs4 import BeautifulSoup
import requests
import pandas as pd


# Team slugs manually taken off of www.pro-football-reference.com
team_slug = ['nwe', 'mia','buf', 'nyj', 'pit', 'rav', 'cin', 'cle', 'htx', \
	'oti', 'clt', 'jax', 'kan', 'rai', 'den', 'sdg', 'dal', 'nyg', 'was', 'phi',\
	'gnb', 'det', 'min', 'chi', 'atl', 'tam', 'nor', 'car', 'sea', 'crd', 'ram', 'sfo']

final_list = []
for slug in team_slug:
	print slug
	response = requests.get("http://www.pro-football-reference.com/teams/"+ slug +"/2016_games.htm")
	soup = BeautifulSoup(response.content, 'lxml')
	lister = []
	for row in soup.find('tbody').find_all('tr')[:17]: #Using "17" limits the scrape to regular season games
		try:
			boxscore = row.find_all('td')[3].find('a')['href']
			lister.append(boxscore[11:23]) # This cuts the slug to the minimum
		except:
			continue
	final_list += lister

# Uses 'set' to remove duplicates and saves the file to csv
pd.DataFrame(list(set(final_list)), columns=['Games']).to_csv('NFL_2016_reg_schedule.csv')