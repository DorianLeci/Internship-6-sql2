import AutoDirectory
import json
import random
from psycopg2.extras import execute_values
from datetime import date,timedelta
import Helper.Overlap as Overlap

def team_player_insert(cur):
    cur.execute("SELECT COUNT(*) FROM team_player")

    if(cur.fetchone()[0]==0):

        cur.execute("SELECT team_id FROM team")
        team_id_list=[row[0] for row in cur.fetchall()]

        cur.execute("SELECT player_id FROM player")
        player_id_list=[row[0] for row in cur.fetchall()]
  
        insert_values=[]
        player_dates={}
        current_team_number={}
        team_has_captain={}

        inserted_pairs=set()

        for player_id in player_id_list:
            chosen_player_id=random.choice(player_id_list)
            
            for _ in range(random.randint(1,4)):
                chosen_team_id=random.choice(team_id_list)

                if((chosen_team_id,chosen_player_id) in inserted_pairs):
                    continue

                date_of_joining=date(2020,1,1)+timedelta(days=random.randint(0,2170))

                if random.random()<0.65:
                    date_of_departure=None
                
                else:
                    if(date_of_joining!=date.today()):
                        daysDiff=(date.today()-date_of_joining).days

                        date_of_departure=date_of_joining+timedelta(days=random.randint(1,daysDiff))
                    else:
                        date_of_departure=None

                period_overlap=any(Overlap.is_there_overlap(s,e,date_of_joining,date_of_departure) for s,e in player_dates.get(player_id,[]))

                if(period_overlap):
                    continue
                
                all_shirt_numbers=ShirtNumberSet()
                availible_numbers=all_shirt_numbers-GetOccupiedShirtNumbers(current_team_number,chosen_team_id,date_of_joining,date_of_departure)

                if(len(availible_numbers)==0):
                    continue
                
                team_has_captain.setdefault(chosen_team_id, False)

                if not team_has_captain[chosen_team_id]:
                    is_captain=random.random()<0.2

                    if(is_captain):
                        team_has_captain[chosen_team_id]=is_captain

                else:
                    is_captain=False
                    
                chosen_shirt_number=random.choice(list(availible_numbers))

                current_team_number.setdefault(chosen_team_id,[])
                current_team_number[chosen_team_id].append((date_of_joining,date_of_departure,chosen_shirt_number))
                
                player_dates.setdefault(player_id,[])
                player_dates[player_id].append((date_of_joining,date_of_departure))

                insert_values.append((date_of_joining,date_of_departure,chosen_shirt_number,is_captain,chosen_team_id,chosen_player_id))

                inserted_pairs.add((chosen_team_id,chosen_player_id))

        execute_values(cur,"INSERT INTO team_player (date_of_joining,date_of_departure,shirt_number,is_captain,team_id,player_id) VALUES %s",insert_values)  

def ShirtNumberSet():
    return set(range(100))

def GetOccupiedShirtNumbers(current_team_number,chosen_team_id,date_of_joining,date_of_departure):

    occupied_shirt_numbers=set()

    for s,e,num in current_team_number.get(chosen_team_id,[]):

        if Overlap.is_there_shirt_number_overlap(s,e,date_of_joining,date_of_departure):
            occupied_shirt_numbers.add(num)

    return occupied_shirt_numbers


