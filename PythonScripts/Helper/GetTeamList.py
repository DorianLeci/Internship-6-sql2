def GetList(cur):
    cur.execute("SELECT team_id FROM team")
    team_id_list=[row[0] for row in cur.fetchall()]

    return team_id_list