import psycopg2
import EntityScripts.Country as Country

def get_data(cur):
    Country.country_insert(cur)



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