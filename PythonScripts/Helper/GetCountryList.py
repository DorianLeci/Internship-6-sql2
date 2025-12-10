def GetList(cur):
    cur.execute("SELECT country_id FROM country")
    country_id_list=[row[0] for row in cur.fetchall()]

    return country_id_list
