from psycopg2.extras import execute_values
import random

def team_tour_insert(cur, team_id_list):

    cur.execute("SELECT COUNT(*) FROM team_tournament_edition")
    if cur.fetchone()[0] > 0:
        return


    cur.execute("SELECT tournament_edition_id, start_date, end_date, num_of_teams FROM tournament_edition")
    tournaments = cur.fetchall()

    insert_values = []

    for edition_id, start_date, end_date, max_teams in tournaments:

        cur.execute("""
            SELECT team_id
            FROM team
            WHERE team_id = ANY(%s)
            AND NOT EXISTS (
                SELECT 1
                FROM team_tournament_edition tte
                JOIN tournament_edition te ON tte.tournament_edition_id = te.tournament_edition_id
                WHERE tte.team_id = team.team_id
                  AND te.start_date <= %s AND te.end_date >= %s
            )
            AND (
                SELECT COUNT(*)
                FROM team_player tp
                WHERE tp.team_id = team.team_id
                  AND tp.date_of_joining <= %s
                  AND (tp.date_of_departure IS NULL OR tp.date_of_departure >= %s)
            ) >= 5
            """, (team_id_list, end_date, start_date, end_date, start_date))

        available_teams = [row[0] for row in cur.fetchall()]
        random.shuffle(available_teams)

        chosen_teams = available_teams[:max_teams]


        insert_values.extend((team_id, edition_id) for team_id in chosen_teams)

    execute_values(
        cur,
        "INSERT INTO public.team_tournament_edition (team_id, tournament_edition_id) VALUES %s",
        insert_values
    )
