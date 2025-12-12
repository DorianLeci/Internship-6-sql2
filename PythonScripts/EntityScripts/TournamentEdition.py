import AutoDirectory
import json
from psycopg2.extras import execute_values
import random
from datetime import date,timedelta
import calendar

def tournament_edition_insert(cur):
    cur.execute("SELECT COUNT(*) FROM tournament_edition")

    if(cur.fetchone()[0]==0):

        MIN_DURATION=3
        MAX_DURATION=14

        cur.execute("SELECT location_id FROM tournament_location")
        location_id_list=[row[0] for row in cur.fetchall()]

        cur.execute("SELECT tournament_id FROM tournament")
        tournament_id_list=[row[0] for row in cur.fetchall()]

        insert_values=[]

        for tid in tournament_id_list:
            availible_years = list(range(2020, 2026))
            location_id=random.choice(location_id_list)
            tournament_id=random.choice(tournament_id_list)

            month=random.randint(1,12)
            
            tournament_duration=random.randint(MIN_DURATION,MAX_DURATION)

            number_of_editions=random.randint(1,6)
            for _ in range(number_of_editions):
                
                year=random.choice(availible_years)
                availible_years.remove(year)

                last_day=calendar.monthrange(year,month)[1]
                last_month_date=date(year,month,last_day)

                start_day=random.randint(1,last_day-tournament_duration+1)

                start_date=date(year,month,start_day)

                end_date = start_date + timedelta(days=tournament_duration-1)

                num_of_teams=random.choice([8,16,32])

                insert_values.append((start_date,end_date,num_of_teams,tournament_id,location_id))

        execute_values(cur,"INSERT INTO public.tournament_edition (start_date,end_date,num_of_teams,tournament_id,location_id) VALUES %s",insert_values)  

        cur.execute(""" DELETE FROM tournament_edition WHERE tournament_edition_id IN
                        (SELECT tournament_edition_id
                         FROM team_tournament_edition
                         GROUP BY tournament_edition_id
                         HAVING COUNT(*) NOT IN (4,8,16,32)
                         )""")