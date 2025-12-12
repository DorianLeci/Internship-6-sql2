import AutoDirectory
import json
from psycopg2.extras import execute_values

def tournament_insert(cur):
    cur.execute("SELECT COUNT(*) FROM tournament_match")

    if(cur.fetchone()[0]==0):

        insert_values=[]

        cur.execute("SELECT tournament_edition_id from tournament_edition")
        
        execute_values(cur,"INSERT INTO public.tournament_match (date_time,tournament_edition_id) VALUES %s",insert_values)  