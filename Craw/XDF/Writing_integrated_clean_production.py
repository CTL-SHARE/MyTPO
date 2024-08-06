import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()

cur.execute("SELECT passage_clean, url FROM tpo.xdf.writing_integrated where passage_json is null")
rows = cur.fetchall()

for row in rows:
    passage = bs(row[0], "html.parser")
    url = row[1]

    passage_json = []
    if passage.find("h2"):
        passage_json.append("@#" + passage.find("h2").get_text(strip=True))

    for p in passage.find_all("p"):
        if p.get_text(strip=True) != '':
            if p.find('span') or len(p.get_text(strip=True)) < 50:
                passage_json.append("##" + p.get_text(strip=True))
            else:
                passage_json.append(p.get_text(strip=True))

    cur.execute("UPDATE tpo.xdf.writing_integrated SET passage_json = %s WHERE url = %s", (str(passage_json), url))
    # conn.commit()
    ...
conn.commit()
