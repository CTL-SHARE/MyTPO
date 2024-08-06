import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()

cur.execute("SELECT prompt_clean, url FROM tpo.xdf.listening_conversation where prompt_text is null")
rows = cur.fetchall()

for row in rows:
    prompt = bs(row[0], "html.parser").get_text(strip=True)
    url = row[1]

    cur.execute("UPDATE tpo.xdf.listening_conversation SET prompt_text = %s WHERE url = %s", (str(prompt), url))
    conn.commit()
