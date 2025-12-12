from psycopg2.extras import execute_values
from datetime import timedelta
import random

GROUP_SIZE=4

def match_insert(cur):
    cur.execute("SELECT COUNT(*) FROM tournament_match")

    if(cur.fetchone()[0]==0):

        insert_values=[]

        cur.execute("SELECT tournament_edition_id,start_date,end_date FROM tournament_edition")
        tour_edit_info=cur.fetchall()

        for tour_edit_id,start_date,end_date in tour_edit_info:
            cur.execute("SELECT match_type_id,phase,number_of_teams FROM match_type WHERE tournament_edition_id=%s",(tour_edit_id,))
            match_types=cur.fetchall()

            for match_type_id,phase,num_of_teams in match_types:

                if phase=='group_stage':
                    num_of_matches=(num_of_teams//GROUP_SIZE)*((GROUP_SIZE*(GROUP_SIZE-1))//2)
                
                else:
                    num_of_matches=num_of_teams//2

                for _ in range(num_of_matches):

                    days_range=(end_date-start_date).days

                    date_time=start_date+timedelta(days=random.randint(0,days_range),hours=random.randint(0,23),minutes=random.choice([0,15,30,45]))
                    insert_values.append((date_time,match_type_id,tour_edit_id))




        execute_values(cur,"INSERT INTO public.tournament_match (date_time,match_type_id,tournament_edition_id) VALUES %s",insert_values)
