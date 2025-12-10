import AutoDirectory
import json

def location_insert(cur,count=1000):
    cur.execute("SELECT COUNT(*) FROM location")

    if(cur.fetchone()[0]==0):
        with open(AutoDirectory.csv_data_path("location.json"), "r") as f:
            country = json.load(f)

        insert_values=[(c["country_name"]) for c in country]

        cur.executemany("INSERT INTO public.country (country_id,country_name) VALUES (%s,%s)",insert_values)  