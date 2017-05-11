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
	df = pd.DataFrame(lister)
	df['team'] = slug
	# df.to_csv(slug + "-" + table_id.replace('"', '') + "2016" + ".csv")
	return df


team_slug = ['nwe', 'mia', 'buf', 'nyj', 'pit', 'rav', 'cin', 'cle', 'htx', \
	'oti', 'clt', 'jax', 'kan', 'rai', 'den', 'sdg', 'dal', 'nyg', 'was', 'phi',\
	'gnb', 'det', 'min', 'chi', 'atl', 'tam', 'nor', 'car', 'sea', 'crd', 'ram', 'sfo']

passing = []
rushing_receiving = []
defense = []
scoring = []
for slug in team_slug:
	print "Working on:", slug
	response = requests.get("http://www.pro-football-reference.com/teams/" + slug + "/2016.htm")
	soup = BeautifulSoup(response.content, 'lxml')
	for table in [['"passing"', 28, 3], ['"div_rushing_and_receiving"', 24, 18], ['"defense"', 18, 44], ['"scoring"', 22, 14]]:
		ans = scrape_page(slug, table)
		
		if table[0] == '"passing"':
			passing.append(ans)
		elif table[0] == '"div_rushing_and_receiving"':
			rushing_receiving.append(ans)
		elif table[0] == '"defense"':
			defense.append(ans)
		elif table[0] == '"scoring"':
			scoring.append(ans)


red_passing = reduce(lambda x, y: pd.concat([x, y], ignore_index=True), passing)
red_rushing = reduce(lambda x, y: pd.concat([x, y], ignore_index=True), rushing_receiving)
red_defense = reduce(lambda x, y: pd.concat([x, y], ignore_index=True), defense)
red_scoring = reduce(lambda x, y: pd.concat([x, y], ignore_index=True), scoring)


red_passing.to_csv("NFL_passing_2016.csv")
red_rushing.to_csv("NFL_rushing_receiving_2016.csv")
red_defense.to_csv("NFL_defense_2016.csv")
red_scoring.to_csv("NFL_scoring_2016.csv")

		