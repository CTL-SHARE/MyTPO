import re

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()

cur.execute(
    "SELECT passage_html, url FROM tpo.xdf.writing_independent where passage_json is null and trash = false order by examid")
rows = cur.fetchall()

for row in rows:
    passage = bs(row[0], "html.parser")
    url = row[1]

    passage_json = []
    match = re.search(r'a class on(.*?)\. Write', passage.get_text(strip=True))
    if match:
        passage_json.append("@#" + match.group(1).strip())

    for i in passage.find_all('p'):
        if i.get_text(strip=True) == '':
            i.decompose()

    for i in passage.find_all('p')[1:-1]:
        passage_json.append(i.get_text(strip=True))

    if '•' in passage_json[0]:
        passage_json = passage_json[3:]

    cur.execute("UPDATE tpo.xdf.writing_independent SET passage_json = %s WHERE url = %s", (str(passage_json), url))
    conn.commit()
