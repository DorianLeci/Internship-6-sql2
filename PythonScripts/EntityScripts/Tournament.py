import AutoDirectory
import json
from psycopg2.extras import execute_values

def tournament_insert(cur):
    cur.execute("SELECT COUNT(*) FROM tournament")

    if(cur.fetchone()[0]==0):
        with open(AutoDirectory.csv_data_path("tournament.json"), "r") as f:
            tournaments = json.load(f)

        insert_values=[(t["name"],t["description"]) for t in tournaments]

        execute_values(cur,"INSERT INTO public.tournament (name,description) VALUES %s",insert_values)  