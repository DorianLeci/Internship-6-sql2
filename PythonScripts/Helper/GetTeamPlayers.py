def get_dict(cur):
    team_players = {}
    cur.execute("SELECT team_id, date_of_joining, date_of_departure FROM team_player")

    for team_id,join,depart in cur.fetchall():
        team_players.setdefault(team_id,[]).append((join,depart))

    return team_players