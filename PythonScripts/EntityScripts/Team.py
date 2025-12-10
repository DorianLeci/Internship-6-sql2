import AutoDirectory
import json
import random
from psycopg2.extras import execute_values

def team_insert(cur,country_id_list):
    cur.execute("SELECT COUNT(*) FROM team")

    if(cur.fetchone()[0]==0):
        with open(AutoDirectory.csv_data_path("team.json"), "r") as f:
            teams = json.load(f)

        insert_values=[(team["team_name"],team["team_email"],team["contact_number"],random.choice(country_id_list)) for team in teams]

        execute_values(cur,"INSERT INTO team (team_name,team_email,contact_number,country_id) VALUES %s",insert_values)  