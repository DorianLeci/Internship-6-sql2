import random
from psycopg2.extras import execute_values
from datetime import date,timedelta
import Helper.Overlap as Overlap

MIN_PLAYERS=50
MAX_PLAYERS=100
MIN_STAY_IN_TEAM=3

def team_player_insert(cur,team_id_list):
    cur.execute("SELECT COUNT(*) FROM team_player")

    if(cur.fetchone()[0]==0):

        cur.execute("SELECT player_id FROM player")
        player_id_list=[row[0] for row in cur.fetchall()]
  
        insert_values=[]
        player_dates={}
        current_team_number={}
        team_has_captain={}

        inserted_pairs=set()

        for team_id in team_id_list:
            num_players = random.randint(MIN_PLAYERS,MAX_PLAYERS)

            available_players=[p for p in player_id_list if (team_id,p) not in inserted_pairs]
            random.shuffle(available_players)
            chosen_players = available_players[:num_players]


            for chosen_player_id in chosen_players:

                            if((team_id,chosen_player_id) in inserted_pairs):
                                continue
                            
                            start_date=date(2020,1,1)
                            date_of_joining=start_date+timedelta(days=random.randint(MIN_STAY_IN_TEAM,(date.today()-start_date).days))

                            if random.random()<0.9:
                                date_of_departure=None
                            
                            else:
                                if(date_of_joining!=date.today()):
                                    daysDiff=(date.today()-date_of_joining).days

                                    date_of_departure=date_of_joining+timedelta(days=random.randint(1,daysDiff))
                                else:
                                    date_of_departure=None

                            period_overlap=any(Overlap.is_there_overlap(s,e,date_of_joining,date_of_departure) for s,e in player_dates.get(chosen_player_id,[]))

                            if(period_overlap):
                                continue
                            
                            all_shirt_numbers=ShirtNumberSet()
                            availible_numbers=all_shirt_numbers-GetOccupiedShirtNumbers(current_team_number,team_id,date_of_joining,date_of_departure)

                            if(len(availible_numbers)==0):
                                continue
                            
                            if(Overlap.has_current_captain(current_team_number,team_id,date_of_joining,date_of_departure)):
                                is_captain=False
                            
                            else:
                                is_captain=random.random()<0.2
                                
                            chosen_shirt_number=random.choice(list(availible_numbers))

                            current_team_number.setdefault(team_id,[])
                            current_team_number[team_id].append((date_of_joining,date_of_departure,chosen_shirt_number,is_captain))
                            
                            player_dates.setdefault(chosen_player_id,[])
                            player_dates[chosen_player_id].append((date_of_joining,date_of_departure))

                            insert_values.append((date_of_joining,date_of_departure,chosen_shirt_number,is_captain,team_id,chosen_player_id))

                            inserted_pairs.add((team_id,chosen_player_id))

        execute_values(cur,"INSERT INTO team_player (date_of_joining,date_of_departure,shirt_number,is_captain,team_id,player_id) VALUES %s",insert_values) 

        cur.execute("""DELETE FROM team_player WHERE team_id IN( SELECT team_id FROM TEAM_PLAYER GROUP BY team_id HAVING COUNT(*)=1)""") 

def ShirtNumberSet():
    return set(range(100))

def GetOccupiedShirtNumbers(current_team_number,chosen_team_id,date_of_joining,date_of_departure):

    occupied_shirt_numbers=set()

    for s,e,num,_ in current_team_number.get(chosen_team_id,[]):

        if Overlap.is_there_overlap_inclusive(s,e,date_of_joining,date_of_departure):
            occupied_shirt_numbers.add(num)

    return occupied_shirt_numbers


