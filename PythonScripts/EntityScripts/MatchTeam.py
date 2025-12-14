from psycopg2.extras import execute_values
from Helper import TournamentStageGenerator as Generator
import random
from itertools import combinations

MAX_SCORED_GOALS=5
TEAMS_TO_ADVANCE=2
GROUP_SIZE=4

def match_team_insert(cur):
    cur.execute("SELECT COUNT(*) FROM match_team")

    if(cur.fetchone()[0]==0):
        
        insert_values=[]

        cur.execute("SELECT tournament_edition_id,num_of_teams FROM tournament_edition")

        tour_edit_info=cur.fetchall()

        for tour_edit_id,num_of_teams in tour_edit_info:

            cur.execute("""SELECT team_id FROM team 
                        WHERE team_id IN(
                        SELECT team_id 
                        FROM team_tournament_edition 
                        WHERE tournament_edition_id=%s
                        )""",(tour_edit_id,))
            
            team_list=[row[0] for row in cur.fetchall()]

            if(len(team_list)==0):
                continue

            print("Team list len: ",len(team_list))

            groups=[team_list[i:i+GROUP_SIZE] for i in range(0,len(team_list),GROUP_SIZE)]

            generate_matches(cur,insert_values,groups,tour_edit_id,team_list)

        execute_values(cur,"INSERT INTO public.match_team (match_id,team_id,score) VALUES %s",insert_values)  

        update_winner(cur)

        caluclate_team_stats(cur)


def generate_matches(cur,insert_values,groups,tour_edit_id,team_list):

    print("Tournament_edition_id: ",tour_edit_id)
    cur.execute("""SELECT tm.match_id FROM tournament_match tm
                    JOIN match_type mt ON mt.match_type_id=tm.match_type_id
                    WHERE tournament_edition_id=%s
                    """,(tour_edit_id,))
    
    matches=[row[0] for row in cur.fetchall()]

    cur.execute("SELECT phase FROM match_type WHERE tournament_edition_id=%s", (tour_edit_id,))
    phase_list =[row[0] for row in cur.fetchall()] 

    match_index=0
    qual_teams=team_list
            
    if "group_stage" in phase_list:
        (qual_teams,match_index)=generate_group_pairs(groups,matches,insert_values)

    knockout_phase_list=[p for p in phase_list if p!="group_stage"]
    generate_knockout_pairs(qual_teams,insert_values,matches,match_index,knockout_phase_list)


def generate_group_pairs(groups,match_list,insert_values,):

    qualified_teams=[]
    match_index=0

    for group in groups:

        all_pairs=list(combinations(group,2))
        print("All pairs length: ",len(all_pairs))
        team_points={team: 0 for team in group}

        for team1,team2 in all_pairs:
                
                print(f"match_index={match_index}, match_list_len={len(match_list)}")               
                match_id=match_list[match_index]

                team1_score=random.randint(0,MAX_SCORED_GOALS)
                team2_score=random.randint(0,MAX_SCORED_GOALS)

                insert_values.append((match_id,team1,team1_score))
                insert_values.append((match_id,team2,team2_score))

                calculate_score(team1_score,team2_score,team_points,team1,team2)

                match_index+=1


        sorted_group=sorted(group,key=lambda x: team_points[x],reverse=True)

        qualified_teams.extend(sorted_group[:TEAMS_TO_ADVANCE])

    return (qualified_teams,match_index)

        
def generate_knockout_pairs(qual_teams,insert_values,match_list,match_index,knockout_phases):
        
        current_round=qual_teams
        semifinal_losers=[]

        for phase in knockout_phases:
            print("Phase: ",phase)
            print(f"match_index={match_index}, match_list_len={len(match_list)}")   
            if phase=="third_place":
                curr_round_pairs=[(semifinal_losers[0],semifinal_losers[1])]
            else:
                winner_list=[]
                curr_round_pairs=[(current_round[i],current_round[i+1]) for i in range(0,len(current_round),2)]

            for team1,team2 in curr_round_pairs:

                match_id=match_list[match_index]

                team1_score=random.randint(0,MAX_SCORED_GOALS)
                team2_score=random.randint(0,MAX_SCORED_GOALS)

                if team1_score==team2_score:
                    if random.random()<0.5:
                        team1_score+=1
                        winner=team1
                    else:
                        team2_score+=1
                        winner=team2
                
                elif team1_score>team2_score:
                    winner=team1
                
                else:
                    winner=team2

                insert_values.append((match_id,team1,team1_score))
                insert_values.append((match_id,team2,team2_score))

                match_index+=1

                if phase == "semifinal":
                    semifinal_losers.append(team1 if winner==team2 else team2)
                
                if phase=="third_place":
                    continue

                winner_list.append(winner)

            current_round=winner_list
                            
def calculate_score(score1,score2,points,team1_id,team2_id):

    if score1>score2:
        points[team1_id]+=3
    
    elif score2>score1:
        points[team2_id]+=3

    else:
        points[team1_id]+=1
        points[team2_id]+=1

def update_winner(cur):
     cur.execute("""UPDATE tournament_match tm 
                    SET winner_id=temp.winner_id
                 
                FROM(
                SELECT mt1.match_id,
                CASE
                    WHEN mt1.score>mt2.score THEN mt1.team_id
                    WHEN mt2.score>mt1.score THEN mt2.team_id
                    ELSE NULL
                END AS winner_id

                FROM match_team mt1
                 
                JOIN match_team mt2 ON mt2.match_id=mt1.match_id
                WHERE mt1.team_id<>mt2.team_id AND mt1.team_id < mt2.team_id
                ) AS temp
                 
                WHERE tm.match_id=temp.match_id""")

def caluclate_team_stats(cur):

   cur.execute("""UPDATE team_tournament_edition tte
                    SET number_of_wins=temp.num_of_wins
                    FROM(
                    SELECT tm.winner_id,mt.tournament_edition_id,COUNT(*) as num_of_wins
                    FROM tournament_match tm
                    JOIN match_type mt ON mt.match_type_id=tm.match_type_id
                    WHERE winner_id IS NOT NULL
                    GROUP BY tm.winner_id,tournament_edition_id
                    ) AS temp
                    WHERE tte.team_id=temp.winner_id AND temp.tournament_edition_id=tte.tournament_edition_id""")
   
   cur.execute("""UPDATE team_tournament_edition tte
                    SET stage_reached=CASE

                        WHEN EXISTS(
                        SELECT 1
                        FROM match_team mt
                        JOIN tournament_match tm ON tm.match_id=mt.match_id
                        JOIN match_type mty ON mty.match_type_id=tm.match_type_id
                        WHERE mty.phase='final' AND mt.team_id=tm.winner_id
                        AND tte.tournament_edition_id=mty.tournament_edition_id
                        AND mt.team_id = tte.team_id
                        ) THEN 'Winner'::ranking

                        WHEN EXISTS(
                        SELECT 1
                        FROM match_team mt
                        JOIN tournament_match tm ON tm.match_id=mt.match_id
                        JOIN match_type mty ON mty.match_type_id=tm.match_type_id
                        WHERE mty.phase='final' AND mt.team_id!=tm.winner_id
                        AND tte.tournament_edition_id=mty.tournament_edition_id
                        AND mt.team_id = tte.team_id) THEN 'Runner-Up'::ranking

                        WHEN EXISTS(
                        SELECT 1
                        FROM match_team mt
                        JOIN tournament_match tm ON tm.match_id=mt.match_id
                        JOIN match_type mty ON mty.match_type_id=tm.match_type_id
                        WHERE mty.phase='third_place' AND mt.team_id=tm.winner_id
                        AND tte.tournament_edition_id=mty.tournament_edition_id
                        AND mt.team_id = tte.team_id) THEN 'Third Place'::ranking

                        WHEN EXISTS(
                        SELECT 1
                        FROM match_team mt
                        JOIN tournament_match tm ON tm.match_id=mt.match_id
                        JOIN match_type mty ON mty.match_type_id=tm.match_type_id
                        WHERE mty.phase IN ('round_of_32','round_of_16','quarterfinal','semifinal')
                        AND tte.tournament_edition_id=mty.tournament_edition_id
                        AND mt.team_id = tte.team_id) THEN 'Knockout Phase'::ranking

                        ELSE 'Group Stage'::ranking
                    END""")
     

