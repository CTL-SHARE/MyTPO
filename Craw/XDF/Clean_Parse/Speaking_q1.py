import re

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()
cur.execute("SELECT examid, full_html FROM tpo.xdf.speaking_q1")
rows = cur.fetchall()

for row in rows:
    html = bs(row[1], "html.parser")

    caption_html = html.find('h3', {'class': 'ul-title'})
    caption_clean = re.sub(r'\s+', ' ', caption_html.text).strip()

    prompt_html = html.find('div', {'class': 'QandA'}).find('p')
    for i in prompt_html.find_all()[1:]:
        i.extract()
    prompt_clean = prompt_html.get_text(strip=True)

    cur.execute(
        "UPDATE tpo.xdf.speaking_q1 SET caption_html = %s, caption_clean = %s, prompt_html = %s, prompt_clean = %s WHERE examid = %s",
        (str(caption_html), caption_clean, str(prompt_html), prompt_clean, str(int(row[0]))))

conn.commit()
conn.close()
