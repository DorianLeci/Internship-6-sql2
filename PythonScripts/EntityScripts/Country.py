import AutoDirectory
import json
from psycopg2.extras import execute_values

def country_insert(cur):
    cur.execute("SELECT COUNT(*) FROM country")

    if(cur.fetchone()[0]==0):
        with open(AutoDirectory.csv_data_path("country.json"), "r") as f:
            country = json.load(f)

        insert_values=[(c["country_name"],) for c in country]

        execute_values(cur,"INSERT INTO public.country (country_name) VALUES %s",insert_values)  