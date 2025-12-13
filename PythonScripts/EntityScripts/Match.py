from psycopg2.extras import execute_values
from datetime import timedelta,datetime
import random

GROUP_SIZE=4

def match_insert(cur):
    cur.execute("SELECT COUNT(*) FROM tournament_match")

    if(cur.fetchone()[0]==0):

        insert_values=[]

        cur.execute("SELECT tournament_edition_id,start_date,end_date FROM tournament_edition")
        tour_edit_info=cur.fetchall()

        cur.execute("SELECT referee_id FROM referee")
        ref_id_list=[row[0] for row in cur.fetchall()]

        for tour_edit_id,start_date,end_date in tour_edit_info:

            cur.execute("""SELECT match_type_id,phase,number_of_teams FROM match_type WHERE tournament_edition_id=%s 
                            ORDER BY CASE phase
                            WHEN 'group_stage' THEN 1
                            WHEN 'round_of_32' THEN 2
                            WHEN 'round_of_16' THEN 3
                            WHEN 'quarterfinal' THEN 4
                            WHEN 'semifinal' THEN 5
                            WHEN 'third_place' THEN 6
                            WHEN 'final' THEN 7
                            END""",(tour_edit_id,))

            match_types=cur.fetchall()

            curr_date_time=datetime.combine(start_date, datetime.min.time())

            for match_type_id,phase,num_of_teams in match_types:

                if phase=='group_stage':
                    num_of_matches=(num_of_teams//GROUP_SIZE)*((GROUP_SIZE*(GROUP_SIZE-1))//2)
                
                else:
                    num_of_matches=num_of_teams//2

                for _ in range(num_of_matches):
                    total_matches=num_of_matches
                    total_hour_range=(datetime.combine(end_date,datetime.max.time())-curr_date_time).days*24
                    
                    max_increment=total_hour_range//total_matches
                    curr_date_time+=timedelta(hours=random.randint(1,max(1, max_increment)),minutes=random.choice([0,15,30,45]))

                    referee_id=random.choice(ref_id_list)

                    insert_values.append((curr_date_time,match_type_id,referee_id))




        execute_values(cur,"INSERT INTO public.tournament_match (date_time,match_type_id,referee_id) VALUES %s",insert_values)
