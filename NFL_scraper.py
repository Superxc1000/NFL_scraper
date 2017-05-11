from bs4 import BeautifulSoup, Comment
import requests
import pandas as pd

def scrape_page(slug, table):
	table_id = table[0]
	width = table[1]
	depth = table[2]
	table = 'id=' + table_id
	
	comments = soup.find_all(string=lambda text:isinstance(text,Comment))
	comment = [c for c in comments if table in c][0]
	data = BeautifulSoup(comment, 'lxml')

	lister = []
	dict1 = {}
	x, y = 0, width
	
	for k in range(depth):
		for row in data.find_all('td')[x:y]:
			dict1[row.get("data-stat")] = str(row.text)
		lister.append(dict1.copy())
		x += width
		y += width
    	dict1 = {}
    	
	pd.DataFrame(lister).to_csv(slug + "-" + table_id.replace('"', '') + "2016" + ".csv")


team_slug = ['nwe', 'mia', 'buf', 'nyj', 'pit', 'rav', 'cin', 'cle', 'htx', \
	'oti', 'clt', 'jax', 'kan', 'rai', 'den', 'sdg', 'dal', 'nyg', 'was', 'phi',\
	'gnb', 'det', 'min', 'chi', 'atl', 'tam', 'nor', 'car', 'sea', 'crd', 'ram', 'sfo']

for slug in team_slug:
	print "Working on:", slug
	response = requests.get("http://www.pro-football-reference.com/teams/" + slug + "/2016.htm")
	soup = BeautifulSoup(response.content, 'lxml')
	for table in [['"passing"', 28, 3], ['"div_rushing_and_receiving"', 24, 18], ['"defense"', 18, 44], ['"scoring"', 22, 14]]:
		scrape_page(slug, table)
