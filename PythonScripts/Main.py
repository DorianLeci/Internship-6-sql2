import psycopg2
import EntityScripts.Country as Country
import EntityScripts.Location as Location
import EntityScripts.Player as Player
import EntityScripts.Referee as Referee
import EntityScripts.Team as Team
import EntityScripts.Tournament as Tournament
import EntityScripts.TournamentEdition as TournamentEdition
import EntityScripts.MatchType as MatchType
from EntityScripts.TeamTournament import team_tour_insert
import EntityScripts.Match as Match
from EntityScripts.MatchTeam import match_team_insert

from EntityScripts.TeamPlayer import team_player_insert 
import Helper.GetCountryList as GetCountryList
import Helper.GetTeamList as GetTeamList
import traceback


def get_data(cur):
    Country.country_insert(cur)

    country_id_list=GetCountryList.GetList(cur)

    Location.location_insert(cur,country_id_list)

    Player.player_insert(cur,country_id_list)

    Referee.referee_insert(cur,country_id_list)

    Team.team_insert(cur,country_id_list)

    team_id_list=GetTeamList.GetList(cur)
    team_player_insert(cur,team_id_list)

    Tournament.tournament_insert(cur)
    TournamentEdition.tournament_edition_insert(cur)

    team_tour_insert(cur,team_id_list)
    
    MatchType.match_type_insert(cur)
    Match.match_insert(cur)
    match_team_insert(cur)





conn=psycopg2.connect(host="localhost",dbname="Internship-6-sql2",user="postgres",password="postgres")
cur=conn.cursor()

try:
    get_data(cur)
    conn.commit()

except Exception as e:
    conn.rollback()
    print("Došlo je do greške, svi unosi su poništeni:", e)
    traceback.print_exc()

finally:
    cur.close()
    conn.close()