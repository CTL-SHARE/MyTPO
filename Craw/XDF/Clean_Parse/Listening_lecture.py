import json
import re

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()

cur.execute(
    "SELECT DISTINCT examid FROM tpo.xdf.listening_lecture WHERE full_html IS NOT NULL AND downloaded = true and parsed is NULL order by examid")

examids = cur.fetchall()


def parse(html):
    question_html = html.find('div', {'class': 'question'}).find('div', {'class': None})

    prompt_clean = ""
    for i in question_html.find_all('p'):
        if 'class' not in i.attrs and len(i.text.replace('\n', '').strip()) > 0:
            # clear all attributes of descendant tags
            for j in i.find_all():
                j.attrs = {}
            i.attrs = {}
            prompt_clean += str(i.prettify())

    choices: list[str] = []
    choices_html = question_html.find_all('li')

    for i in choices_html:
        choices.append(re.sub(r'\s+', ' ', i.text).strip())

    answers = [question_html.find('div', {'class': 'iradio_square-blue icheck-radio checked disabled'}).find('input')[
                   "id"].replace("answer", "")]

    audio_url = [html.find('audio', {'id': 'listenAudio'})['src'], html.find('audio', {'id': 'audio'})['src']]

    if "暂无原文" in html.find('div', {'role': 'tabpanel'}).text:
        transcription = None
    else:
        transcription = html.find('div', {'role': 'tabpanel'}).text.replace("\n\n", "").replace("\t", ": ").replace(
            "  ", "").strip()

    cur.execute(
        "UPDATE tpo.xdf.listening_lecture SET question_html = %s, prompt_clean = %s, choices = %s, answers = %s, audio_url = %s, audio_download = false, transcription = %s, parsed = true WHERE examid = %s and audioid = %s and num = %s",
        (str(question_html.prettify()), str(prompt_clean), choices, answers, audio_url, transcription,
         str(int(examid[0])), str(int(audioid[0])),
         str(int(question[0]))))


for examid in examids:
    cur.execute("SELECT DISTINCT audioid FROM tpo.xdf.listening_lecture WHERE examid = %s", (str(int(examid[0])),))
    audioids = cur.fetchall()

    for audioid in audioids:
        cur.execute(
            "SELECT DISTINCT num, full_html FROM tpo.xdf.listening_lecture WHERE examid = %s and audioid = %s",
            (str(int(examid[0])), str(int(audioid[0]))))
        questions = cur.fetchall()

        for question in questions:
            try:
                html = bs(question[1], 'html.parser')

                caption_html = html.find('ul', {'class': 'ul-title'})
                caption_clean = re.sub(r'\s+', ' ', caption_html.text).strip()

                cur.execute(
                    "UPDATE tpo.xdf.listening_lecture SET caption_html = %s, caption_clean = %s WHERE examid = %s and audioid = %s and question_index = %s",
                    (str(caption_html), str(caption_clean), str(int(examid[0])),
                     str(int(audioid[0])), str(int(question[0]))))
                parse(html)

                conn.commit()

                print(f"{examid[0]}-{audioid[0]}-{question[0]}, parsed successfully")

            except Exception as e:
                exceptions = json.load(open("Exceptions/listening_lecture.json", "r"))
                exceptions["SQL"].append([f"{examid[0]}-{audioid[0]}-{question[0]}", f"{e}"])

conn.close()
