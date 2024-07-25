import re

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()
cur.execute("SELECT examid, full_html FROM tpo.xdf.writing_independent")
rows = cur.fetchall()

for row in rows:
    html = bs(row[1], "html.parser")

    caption_html = html.find('h3', {'class': 'ul-title'})
    caption_clean = re.sub(r'\s+', ' ', caption_html.text).strip()

    prompt_html = html.find('div', {'class': 'QandA'})
    prompt_clean = prompt_html.find('div', {'class': None}).text.replace("  ", "").replace("\n\n", "").strip()

    cur.execute(
        "UPDATE tpo.xdf.writing_independent SET caption_html = %s, caption_clean = %s, passage_html = %s, passage_clean = %s WHERE examid = %s",
        (str(caption_html), caption_clean, str(prompt_html), prompt_clean, int(int(row[0]))))

conn.commit()
conn.close()
