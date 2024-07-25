import re

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()
cur.execute("SELECT examid, full_html FROM tpo.xdf.speaking_q4")
rows = cur.fetchall()

for row in rows:
    html = bs(row[1], "html.parser")

    caption_html = html.find('h3', {'class': 'ul-title'})
    caption_clean = re.sub(r'\s+', ' ', caption_html.text).strip()

    audio_url = [i['src'] for i in html.find_all('audio', {'id': 'listenAudio'})]

    if "暂无原文" in html.find('div', {'role': 'tabpanel'}).text:
        transcription = None
    else:
        transcription = html.find('div', {'role': 'tabpanel'}).text.replace("\n\n", "").replace("\t", ": ").replace(
            "  ", "").strip()

    cur.execute(
        "UPDATE tpo.xdf.speaking_q4 SET caption_html = %s, caption_clean = %s, audio_url = %s, audio_download = false, transcription = %s WHERE examid = %s",
        (str(caption_html), caption_clean, audio_url, transcription, str(int(row[0]))))

conn.commit()
conn.close()
