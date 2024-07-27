import re

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()

cur.execute(
    "SELECT url, full_html, examid, audioid, question_index FROM tpo.xdf.listening_lecture WHERE parsed is NULL order by examid, audioid, num")

questions = cur.fetchall()


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

    answers = [answer.find('input')["id"].replace("answer", "") for answer in
               question_html.find_all('div', {'class': 'icheckbox_square-blue icheck-checkbox checked disabled'})]

    audio_url = [html.find('audio', {'id': 'listenAudio'})['src'], html.find('audio', {'id': 'audio'})['src']]

    if "暂无原文" in html.find('div', {'role': 'tabpanel'}).text:
        transcription = None
    else:
        transcription = html.find('div', {'role': 'tabpanel'}).text.replace("\n\n", "").replace("\t", ": ").replace(
            "  ", "").strip()

    cur.execute(
        "UPDATE tpo.xdf.listening_lecture SET question_html = %s, prompt_clean = %s, choices = %s, answers = %s, audio_url = %s, audio_download = false, transcription = %s, parsed = true WHERE url = %s",
        (str(question_html.prettify()), str(prompt_clean), choices, answers, audio_url, transcription,
         question[0]))


for question in questions:
    try:
        html = bs(question[1], 'html.parser')

        caption_html = html.find('ul', {'class': 'ul-title'})
        caption_clean = re.sub(r'\s+', ' ', caption_html.text).strip()

        cur.execute(
            "UPDATE tpo.xdf.listening_lecture SET caption_html = %s, caption_clean = %s WHERE url = %s",
            (str(caption_html), str(caption_clean), question[0]))
        parse(html)

        conn.commit()

        print(f"{str(int(question[2]))}-{str(int(question[3]))}-{str(int(question[4]))}, parsed successfully")

    except Exception as e:
        pass

conn.close()
