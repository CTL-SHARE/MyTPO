# [-1] catagorizing questions
import re

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()

cur.execute(
    "SELECT url, full_html FROM tpo.xdf.reading WHERE parsed = false ORDER BY examid, pid, question_index")  # null = unvisited, true = successful, false = fail
questions = cur.fetchall()

for question in questions:
    url = question[0]

    html = bs(question[1], 'html.parser')

    caption_html = html.find('ul', {'class': 'ul-title'})
    caption_clean = re.sub(r'\s+', ' ', caption_html.text).strip()  # text format

    passage_html = html.find('div', {'id': 'js_passage'}).find('div', {'class': 'en'})

    for img in passage_html.find_all('img'):
        img.decompose()

    for span in passage_html.find_all('span'):
        span.attrs = {}

    passage_clean = str(passage_html.prettify())  # html format

    question_html = html.find('div', {'class': 'question'}).find('div', {'class': None})

    prompt_clean = ""  # html format
    for i in question_html.find_all('p'):
        if 'class' not in i.attrs and len(i.text.replace('\n', '').strip()) > 0:
            # clear all attributes of descendant tags
            for j in i.find_all():
                j.attrs = {}
            i.attrs = {}
            prompt_clean += str(i.prettify())

    choices = [re.sub(r'\s+', ' ', choice.text).strip() for choice in question_html.find_all('li')]

    answers = list(
        question_html.find('p', {'class': 'right-answer'}).text.replace('正确答案：', '').strip().replace(' ', ''))

    cur.execute(
        "UPDATE tpo.xdf.reading SET caption_html = %s, caption_clean = %s, passage_html = %s, passage_clean = %s, question_html = %s, prompt_clean = %s, choices = %s, answers = %s, parsed = true WHERE url = %s",
        ((str(caption_html), caption_clean, str(passage_html), passage_clean, str(question_html), prompt_clean,
          choices, answers, url)))
    conn.commit()
