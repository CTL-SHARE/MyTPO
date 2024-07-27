# delete extra img tags
import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()
cur.execute("SELECT examid, passage_clean FROM tpo.xdf.writing_integrated")
rows = cur.fetchall()

for row in rows:
    passage_clean = bs(row[1], "html.parser")

    for img in passage_clean.find_all('img'):
        img.decompose()

    cur.execute("UPDATE tpo.xdf.writing_integrated SET passage_clean = %s where examid = %s",
                (str(passage_clean), str(int(row[0]))))

conn.commit()
conn.close()
