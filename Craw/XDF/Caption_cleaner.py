# Remove redundant test type
import psycopg2

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()

l = {"reading": "Reading ", "listening_conversation": "Listening ", "listening_lecture": "Listening ",
     "speaking_q1": "Speaking ", "speaking_q2": "Speaking ", "speaking_q3": "Speaking ",
     "speaking_q4": "Speaking ", "writing_independent": "Writing ", "writing_integrated": "Writing "}

for i in list(l.keys()):
    cur.execute(f"SELECT caption_clean, url FROM tpo.xdf.{i} order by examid")
    rows = cur.fetchall()
    for row in rows:
        caption = row[0].replace(l[i], '')
        cur.execute(f"UPDATE tpo.xdf.{i} SET caption_clean = %s WHERE url = %s", (caption, row[1]))
        conn.commit()
