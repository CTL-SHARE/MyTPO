import json
import re

import psycopg2
from bs4 import BeautifulSoup as bs

error_questions: list[str] = json.load(open("../Clean_Parse/Exceptions/reading.json", 'r'))['questions']

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()


def normal_multiple_choice(html):  # normal multiple choices
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

    cur.execute(
        "UPDATE tpo.xdf.reading SET question_html = %s, prompt_clean = %s, choices = %s, answers = %s, parsed = true WHERE url = %s",
        (str(question_html.prettify()), str(prompt_clean), choices, answers, q[0]))


for question in error_questions:
    examid = list(question[0].split("-"))[0]
    pid = list(question[0].split("-"))[1]
    question_index = list(question[0].split("-"))[2]

    cur.execute(
        "SELECT url, full_html FROM tpo.xdf.reading WHERE parsed = false and examid = %s and pid = %s and question_index = %s",
        (examid, pid, question_index))

    if not cur.fetchall():
        continue

    q = cur.fetchall()[0]

    html = bs(q[1], 'html.parser')

    caption_html = html.find('ul', {'class': 'ul-title'})

    caption_clean = re.sub(r'\s+', ' ', caption_html.text).strip()

    passage_html = html.find('div', {'id': 'js_passage'}).find('div', {'class': 'en'})

    for i in passage_html.find_all('span'):
        del i['class']
    for i in passage_html.find_all('img'):
        del i['class']
        del i['style']

    passage_clean = re.sub(r'\s+', ' ', str(passage_html)).strip()

    cur.execute(
        "UPDATE tpo.xdf.reading SET caption_html = %s, caption_clean = %s, passage_html = %s, passage_clean = %s WHERE url = %s",
        (str(caption_html), str(caption_clean), str(passage_html), str(passage_clean), str(q[0])))

    normal_multiple_choice(html)

    print(f"{examid}-{pid}-{question_index}: successful")

    conn.commit()
