import sqlite3

def connect_to_database(db_file):
	"""Create a connection to a SQLite Database. The Data base of choice must be imported"""
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()
	return 	conn, cur

def close_to_database(conn):
	"""Closes a connection to a SQLite Database. The connection must be imported"""
	conn.close()
	return

def getting_team_names(cur):
	"""Creating a list of team names from a database."""
	cur.execute("SELECT * FROM Team_Names")
	names = cur.fetchall()
	team_names = [team[0] for team in names]
	return team_names

def loading_team_stats(cur,team_names,year):
	"""Loading team stats for up to (if applicable) the previous three years from a database."""
	### If not between 2018 (Year Coming up) and 2008 (First year of data I have). There is no/not enough data
	if not 2008 < year <= 2018: 
		print('\n Insufficient data for the year you selected. \n')
		return None
	
	### The data I have starts at 2008. Therefore, if before 2010, I do not have three years of data.
	### The times 2 is because I have stats for and against.
	num_of_rows = str((year - 2009 + 1)*2)        ### EX: If year is 2009, we still have data from 2008
	if int(num_of_rows) > 6: num_of_rows = '6'	  ### We only want to use the last three years of data
	
	if year in [2008,2009,2010,2011]: offset_rows = '0' ### If year is at or before 2010, we want all data up to but excluding that year
	else: offset_rows = str((year - 2011)*2)

	team_stats = {}
	for team in team_names:
		### Getting data
		cur.execute("SELECT * FROM team_stats_" + team + " LIMIT " + num_of_rows + " OFFSET " + offset_rows)
		team_stats[team] = cur.fetchall()

	return team_stats

def getting_current_rosters(cur,team_names,year):
	"""Loading past and current team rosters from a database."""
	### If not between 2018 (Year Coming up) and 2008 (First year of data I have). There is no/not enough data
	if not 2008 <= year <= 2018: 
		print('\n Insufficient data for the year you selected. \n')
		return None
	
	### Roster years data collection, first year of data is 2008, 2019 is a couple years out
	years = [str(years) for years in range(year-3,year+1) if 2007 < years < 2019] 

	### 2018 is the current year that is coming up
	if year == 2018:
		### Creating dictionary of current and past rosters for 2018
		current_rosters = {}
		past_rosters = {}
		for team in team_names:
			### Getting data from current rosters
			cur.execute("SELECT * FROM current_rosters_" + team)
			current_rosters[team] = cur.fetchall()

			for past_year in years[:-1]:
				## Getting data from past rosters
				cur.execute("SELECT * FROM past_rosters_" + team + '_' + past_year)
				past_rosters[team] = cur.fetchall()
	else:
		### Creating dictionary of current and past rosters for 2018
		current_rosters = {}
		past_rosters = {}
		for team in team_names:
			### Getting data from current rosters
			cur.execute("SELECT * FROM past_rosters_" + team + '_' + years[-1])
			current_rosters[team] = cur.fetchall()

			for past_year in years[:-1]:
				## Getting data from past rosters
				cur.execute("SELECT * FROM past_rosters_" + team + '_' + past_year)
				past_rosters[team + '_' + past_year] = cur.fetchall()

	return current_rosters, past_rosters

def getting_bio_and_combine_info(cur):
	"""Creating a dictionary for player's bio and draft informaion."""	

	### Will need all positions
	position = ['QB','RB','WR','TE']

	### Getting bio and draft information from the database and placing it in a dictionary
	bio_and_combine = {}
	for pos in position:	
		cur.execute("SELECT * FROM bio_and_combine_info_" + pos + "s")
		bio_and_combine[pos] = cur.fetchall()

	return bio_and_combine

def getting_players_stats(cur):
	"""Creating a dictionary for player's bio and draft informaion."""	

	### Getting passing stats for QB's from database and putting them in a dictionary
	### QB's have two tables, passing and rushing
	player_stats = {}
	cur.execute("SELECT * FROM player_stats_QBs_passing")
	player_stats['QB_passing'] = cur.fetchall()

	### Getting rushing stats for QB's from database and putting them in a dictiona
	cur.execute("SELECT * FROM player_stats_QBs_rushing")
	player_stats['QB_rushing'] = cur.fetchall()

	### Getting stats information from the database for all positions but QB's and placing it in a dictionary
	position = ['RB','WR','TE']
	for pos in position:	
		cur.execute("SELECT * FROM player_stats_" + pos + "s")
		player_stats[pos] = cur.fetchall()

	return player_stats




