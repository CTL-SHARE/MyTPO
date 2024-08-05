import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()

cur.execute("SELECT passage_clean, url FROM tpo.xdf.speaking_q3 where passage_json is null")
rows = cur.fetchall()

for row in rows:
    passage = bs(row[0], "html.parser")
    url = row[1]

    passage_json = []
    for i in passage.find_all()[1:]:
        if i.get_text(strip=True) != '':
            passage_json.append(i.get_text(strip=True))

    cur.execute("UPDATE tpo.xdf.speaking_q3 SET passage_json = %s WHERE url = %s", (str(passage_json), url))
    conn.commit()
