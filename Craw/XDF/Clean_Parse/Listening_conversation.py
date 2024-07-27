# renewed parse methods, write to new db copy
import re

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()

cur.execute(
    "SELECT url, full_html FROM tpo.xdf.listening_conversation WHERE parsed is null ORDER BY examid, audioid, num")  # null = unvisited, true = successful, false = fail
questions = cur.fetchall()

for question in questions:
    url = question[0]

    try:
        html = bs(question[1], 'html.parser')

        caption_html = html.find('ul', {'class': 'ul-title'})
        caption_clean = re.sub(r'\s+', ' ', caption_html.text).strip()  # text format

        question_html = html.find('div', {'class': 'question'}).find('div', {'class': None})

        ul = question_html.find('ul')

        if ul.find('table'):  # table
            choices = []
            answers = []
            for th in ul.find('table').find_all('tr')[0].find_all('th'):
                choices.append(re.sub(r'\s+', ' ', th.text).strip())
            choices.append('#')

            for tr in ul.find_all('table')[0].find_all('tr')[1:]:
                choices.append(re.sub(r'\s+', ' ', tr.find('th').text).strip())
                for td in tr.find_all('td'):
                    if td.find_all('span', attrs=True):
                        answers.append(td['data-aid'])
                        break
        else:  # choiced
            choices = [re.sub(r'\s+', ' ', choice.text).strip() for choice in question_html.find_all('li')]
            if question_html.find_all(class_='icheckbox_square-blue icheck-checkbox checked disabled'):  # n_m
                answers = [answer.find('input')["id"].replace("answer", "") for answer in
                           question_html.find_all(class_='icheckbox_square-blue icheck-checkbox checked disabled')]
            else:  # n_1
                answers = [question_html.find(class_='iradio_square-blue icheck-radio checked disabled').find('input')[
                               "id"].replace("answer", "")]

        for img in question_html.find_all('img'):
            img.decompose()

        for span in question_html.find_all('span'):
            span.attrs = {}

        prompt_clean = ""  # html format
        for i in question_html.find_all('p'):
            if 'class' not in i.attrs and len(i.text.replace('\n', '').strip()) > 0:
                # clear all attributes of descendant tags
                for j in i.find_all():
                    j.attrs = {}
                i.attrs = {}
                prompt_clean += str(i.prettify())

        if "暂无原文" in html.find('div', {'role': 'tabpanel'}).text:
            transcription = None
        else:
            transcription = html.find('div', {'role': 'tabpanel'}).text.replace("\n\n", "").replace("\t", ": ").replace(
                "  ", "").strip()

        prompt_audio_url = html.find('audio', {'id': 'audio'})['src']
        listening_audio_url = html.find('audio', {'id': 'listenAudio'})['src']

        cur.execute(
            "UPDATE tpo.xdf.listening_conversation SET caption_html = %s, caption_clean = %s, question_html = %s, prompt_clean = %s, choices = %s, answers = %s, transcription = %s, prompt_audio_url = %s, listening_audio_url = %s, parsed = true WHERE url = %s",
            (str(caption_html), caption_clean, str(question_html), prompt_clean, choices, answers, transcription,
             str(prompt_audio_url), str(listening_audio_url), url))
        conn.commit()

    except Exception as e:
        print("Error with: ", url)
        cur.execute("UPDATE tpo.xdf.listening_conversation SET parsed = false WHERE url = %s", (url,))
        conn.commit()

conn.close()
