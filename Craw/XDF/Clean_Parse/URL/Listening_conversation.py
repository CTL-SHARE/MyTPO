from urllib.parse import urlparse, parse_qs

import psycopg2

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()
cur.execute(
    "SELECT DISTINCT examid FROM tpo.xdf.listening_conversation WHERE full_html IS NOT NULL AND downloaded = true ORDER BY examid")

examids = cur.fetchall()

for examid in examids:
    cur.execute(
        "SELECT url FROM tpo.xdf.listening_conversation WHERE examid = %s AND full_html IS NOT NULL AND downloaded = true ORDER BY question_index",
        (examid[0],))
    rows = cur.fetchall()

    for row in rows:
        url = row[0]
        num = parse_qs(urlparse(url).query)['num'][0]
        audioId = parse_qs(urlparse(url).query)['audioId'][0]
        cur.execute("UPDATE tpo.xdf.listening_conversation SET num = %s, audioid = %s WHERE url = %s",
                    (num, audioId, url))
        conn.commit()

conn.close()
