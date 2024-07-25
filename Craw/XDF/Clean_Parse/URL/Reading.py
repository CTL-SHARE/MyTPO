from urllib.parse import urlparse, parse_qs

import psycopg2

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()
cur.execute(
    "SELECT DISTINCT examid FROM tpo.xdf.reading WHERE full_html IS NOT NULL AND downloaded = true ORDER BY examid")

examids = cur.fetchall()

for examid in examids:
    cur.execute(
        "SELECT url FROM tpo.xdf.reading WHERE examid = %s AND full_html IS NOT NULL AND downloaded = true ORDER BY question_index",
        (examid[0],))
    rows = cur.fetchall()

    for row in rows:
        url = row[0]
        pId = parse_qs(urlparse(url).query)['pId'][0]
        cur.execute("UPDATE tpo.xdf.reading SET pid = %s WHERE url = %s", (pId, url))
        conn.commit()

conn.close()
