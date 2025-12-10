import AutoDirectory
import json
import random
from psycopg2.extras import execute_values

def location_insert(cur,country_id_list):
    cur.execute("SELECT COUNT(*) FROM tournament_location")

    if(cur.fetchone()[0]==0):
        with open(AutoDirectory.csv_data_path("location.json"), "r") as f:
            city = json.load(f)

        insert_values=[(c["city_name"],c["city_postal_code"],random.choice(country_id_list)) for c in city]

        execute_values(cur,"INSERT INTO public.tournament_location (city_name,city_postal_code,country_id) VALUES %s",insert_values)  