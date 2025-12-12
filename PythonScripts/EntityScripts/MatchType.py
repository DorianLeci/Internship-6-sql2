import AutoDirectory
import json
from psycopg2.extras import execute_values
from Helper import TournamentStageGenerator as Generator
import random

def match_type_insert(cur):
    cur.execute("SELECT COUNT(*) FROM match_type")

    if(cur.fetchone()[0]==0):
        
        insert_values=[]

        cur.execute("SELECT tournament_edition_id,num_of_teams from tournament_edition")
        edition_info_list=cur.fetchall()

        for edition_id,num_of_teams in edition_info_list:

            include_group_stage=random.random()<0.5
            include_third_place_match=random.random()<0.5

            phase_list=Generator.generate_match_type(num_of_teams,include_group_stage,include_third_place_match)

            for phase in phase_list:
                insert_values.append((phase.value,num_of_teams,edition_id))

                if(phase!=Generator.MatchType.THIRD_PLACE and phase!=Generator.MatchType.FINAL):
                    num_of_teams/=2


        execute_values(cur,"INSERT INTO public.match_type (phase,number_of_teams,tournament_edition_id) VALUES %s",insert_values)  