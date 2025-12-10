import AutoDirectory
import json
import random
from psycopg2.extras import execute_values

def player_insert(cur,country_id_list):
    cur.execute("SELECT COUNT(*) FROM player")

    if(cur.fetchone()[0]==0):
        with open(AutoDirectory.csv_data_path("player.json"), "r") as f:
            players = json.load(f)

        insert_values=[(player["player_fname"],player["player_lname"],player["birth_date"],player["height"],
                    player["weight"],player["is_injured"],random.choice(country_id_list)) for player in players]

        execute_values(cur,"INSERT INTO player (player_fname,player_lname,birth_date,height,weight,is_injured,country_id) VALUES %s",insert_values)  