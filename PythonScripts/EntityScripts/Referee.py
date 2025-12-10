import AutoDirectory
import json
import random
from psycopg2.extras import execute_values

def referee_insert(cur,country_id_list):
    cur.execute("SELECT COUNT(*) FROM referee")

    if(cur.fetchone()[0]==0):
        with open(AutoDirectory.csv_data_path("referee.json"), "r") as f:
            referees = json.load(f)

        insert_values=[(ref["referee_fname"],ref["referee_lname"],ref["birth_date"],ref["licence"],random.choice(country_id_list)) for ref in referees]

        execute_values(cur,"INSERT INTO referee (referee_fname,referee_lname,birth_date,licence,country_id) VALUES %s",insert_values)  