import psycopg2
import EntityScripts.Country as Country
import EntityScripts.Location as Location
import EntityScripts.Player as Player
import EntityScripts.Referee as Referee
import Helper.GetCountryList as GetCountryList

def get_data(cur):
    Country.country_insert(cur)

    country_id_list=GetCountryList.GetList(cur)

    Location.location_insert(cur,country_id_list)
    Player.player_insert(cur,country_id_list)
    Referee.referee_insert(cur,country_id_list)



conn=psycopg2.connect(host="localhost",dbname="Internship-6-sql2",user="postgres",password="postgres")
cur=conn.cursor()

try:
    get_data(cur)
    conn.commit()

except Exception as e:
    conn.rollback()
    print("Došlo je do greške, svi unosi su poništeni:", e)

finally:
    cur.close()
    conn.close()