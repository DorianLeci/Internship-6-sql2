from psycopg2.extras import execute_values
import random
from enum import Enum

class EventType(Enum):
    GOAL="goal"
    YELLOW_CARD="yellow_card"
    RED_CARD="red_card"
    SUBSTITUTION="substitution"
    ASSIST="assist"


MIN_MINUTE=1
MAX_MINUTE=90

def match_event_insert(cur):

    cur.execute("SELECT COUNT(*) FROM match_event")

    if(cur.fetchone()[0]==0):
        
        insert_values=[]

        cur.execute("""SELECT tm.match_id, mt.number_of_teams, mt.tournament_edition_id,tm.date_time
                        FROM tournament_match tm
                        JOIN match_type mt ON tm.match_type_id = mt.match_type_id""")
        
        matches=cur.fetchall()

        for match_id,num_of_teams,tour_edit_id,match_date_time in matches:

            cur.execute("SELECT team_id,score FROM match_team WHERE match_id=%s",(match_id,))

            team_score=cur.fetchall()

            for team_id,score in team_score:

                cur.execute("""SELECT tp.player_id
                               FROM team_player tp
                               JOIN team_tournament_edition tte
                               ON tte.team_id = tp.team_id
                               AND tte.tournament_edition_id = %s
                               WHERE tp.team_id = %s""",(tour_edit_id,team_id,))
                
                avaliable_players=[row[0] for row in cur.fetchall()]

                subs=subs_gen(avaliable_players,insert_values,match_id)
                subs=cards_gen(avaliable_players,insert_values,match_id,subs)

                score_gen(avaliable_players,insert_values,match_id,score,subs)

        execute_values(cur,"INSERT INTO public.match_event (event,match_minute,player_id,match_id) VALUES %s",insert_values)





def subs_gen(players,insert_values,match_id):
    subs={}

    num_subs=min(random.randint(1,3),len(players))
                    
    sub_players=random.sample(players,num_subs)
    for sub_player in sub_players:

        sub_minute=random.randint(MIN_MINUTE,MAX_MINUTE)
        subs[sub_player]=sub_minute

        insert_values.append((EventType.SUBSTITUTION.value,sub_minute,sub_player,match_id))
    
    return subs

def score_gen(players,insert_values,match_id,score,subs):

    for _ in range(score):

        scorer_id=random.choice(players)

        exit_minute=subs.get(scorer_id,MAX_MINUTE)
        match_minute=random.randint(MIN_MINUTE,exit_minute)

        insert_values.append((EventType.GOAL.value,match_minute,scorer_id,match_id))

        potential_assisters=[p for p in players if p!=scorer_id and subs.get(p,MAX_MINUTE)>=match_minute]

        if potential_assisters:
            assister_id=random.choice(potential_assisters)
            insert_values.append((EventType.ASSIST.value,match_minute,assister_id,match_id))



def cards_gen(players,insert_values,match_id,subs):
    
    player_yellow={p: 0 for p in players}

    for p in players:
        
        if player_yellow[p]<2 and random.random()<0.1: #red_card
            exit_minute=subs.get(p,MAX_MINUTE)
            match_minute=random.randint(MIN_MINUTE,exit_minute)

            subs[p]=match_minute
            insert_values.append((EventType.RED_CARD.value,match_minute,p,match_id))
            continue

        if random.random()<0.3: #yellow_card
            
            exit_minute=subs.get(p,MAX_MINUTE)
            match_minute=random.randint(MIN_MINUTE,exit_minute)

            player_yellow[p]+=1
            insert_values.append((EventType.YELLOW_CARD.value,match_minute,p,match_id))

            if(player_yellow[p]==2):
                insert_values.append((EventType.RED_CARD.value,match_minute,p,match_id))
                subs[p]=match_minute
            
    return subs
        
