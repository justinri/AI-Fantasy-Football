from loading_data import *
import sys

def get_data(year):
	## Year is for the year you want the results for, is only for testing
	db_file = 'databases/info_database.db'

	### Opening Connection to database
	[conn, cur] = connect_to_database(db_file)

	### Getting Team names
	team_names = getting_team_names(cur)

	### Getting team stats and placing them in a dictionary
	team_stats = loading_team_stats(cur,team_names,year)

	### Getting past and current rosters
	[current_rosters, past_rosters] = getting_current_rosters(cur,team_names,year)

	### Getting all players bio and combine inforomation
	bio_and_combine = getting_bio_and_combine_info(cur)

	### Getting all players stats
	players_stats = getting_players_stats(cur)

	### closing Connection to database
	close_to_database(conn)

	return team_names, team_stats, current_rosters, past_rosters, bio_and_combine, players_stats

if __name__ == '__main__':
	year = 2017
	[team_names, team_stats, current_rosters, past_rosters, bio_and_combine, players_stats] = get_data(year)
