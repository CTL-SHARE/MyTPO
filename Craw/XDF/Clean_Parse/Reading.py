import json
import re

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()
# SELECT * FROM tpo.xdf.reading WHERE downloaded=true and question_index is NULL  ->  misplaced writing question, delete from reading table

cur.execute(
    "SELECT DISTINCT examid FROM tpo.xdf.reading WHERE full_html IS NOT NULL AND downloaded = true and parsed is NULL order by examid")

examids = cur.fetchall()


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

    answers = [question_html.find('div', {'class': 'iradio_square-blue icheck-radio checked disabled'}).find('input')[
                   "id"].replace("answer", "")]

    cur.execute(
        "UPDATE tpo.xdf.reading SET question_html = %s, prompt_clean = %s, choices = %s, answers = %s, parsed = true WHERE examid = %s and pid = %s and question_index = %s",
        (str(question_html.prettify()), str(prompt_clean), choices, answers, str(int(examid[0])), str(int(pid[0])),
         str(int(question[0]))))


def insert_line(html):  # insert a sentence in paragraph [-2]
    question_html = html.find('div', {'class': 'question'}).find('div', {'class': None})

    prompt_clean = ""
    for i in question_html.find_all('p'):
        if 'class' not in i.attrs and len(i.text.replace('\n', '').strip()) > 0:
            # clear all attributes of descendant tags
            for j in i.find_all():
                j.attrs = {}
            i.attrs = {}
            prompt_clean += str(i.prettify())

    answers = [question_html.find('p', {'class': 'right-answer'}).text.replace('正确答案：', '').strip()]

    choices = ["inline"]

    cur.execute(
        "UPDATE tpo.xdf.reading SET question_html = %s, prompt_clean = %s, choices = %s, answers = %s, parsed = true WHERE examid = %s and pid = %s and question_index = %s",
        (str(question_html.prettify()), str(prompt_clean), choices, answers, str(int(examid[0])), str(int(pid[0])),
         str(int(question[0]))))


def multi_select(html):  # general meaning [-1]
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

    answers = list(question_html.find('p', {'class': 'right-answer'}).text.replace('正确答案：', '').strip().split(' '))

    cur.execute(
        "UPDATE tpo.xdf.reading SET question_html = %s, prompt_clean = %s, choices = %s, answers = %s, parsed = true WHERE examid = %s and pid = %s and question_index = %s",
        (str(question_html.prettify()), str(prompt_clean), choices, answers, str(int(examid[0])), str(int(pid[0])),
         str(int(question[0]))))


for examid in examids:
    cur.execute("SELECT DISTINCT pid FROM tpo.xdf.reading WHERE examid = %s", (str(int(examid[0])),))
    pids = cur.fetchall()

    for pid in pids:
        cur.execute("SELECT DISTINCT question_index, full_html FROM tpo.xdf.reading WHERE examid = %s and pid = %s",
                    (str(int(examid[0])), str(int(pid[0]))))
        questions = cur.fetchall()

        if len(questions) == 10:
            last_second = 9
            last_first = 10
        elif len(questions) == 14:
            last_second = 13
            last_first = 14
        else:
            exceptions = json.load(open("Exceptions/reading.json", "r"))
            exceptions["passages"].append(f"{examid[0]}-{pid[0]}")
            json.dump(exceptions, open("Exceptions/reading.json", "w"))
            cur.execute("UPDATE tpo.xdf.reading SET parsed = false WHERE examid = %s and pid = %s",
                        (str(int(examid[0])), str(int(pid[0]))))
            continue

        for question in questions:
            try:
                html = bs(question[1], 'html.parser')

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
                    "UPDATE tpo.xdf.reading SET caption_html = %s, caption_clean = %s, passage_html = %s, passage_clean = %s WHERE examid = %s and pid = %s and question_index = %s",
                    (str(caption_html), str(caption_clean), str(passage_html), str(passage_clean), str(int(examid[0])),
                     str(int(pid[0])), str(int(question[0]))))

                if int(question[0]) == last_second:
                    try:
                        insert_line(html)
                        print(f"{examid[0]}-{pid[0]}-{question[0]}")
                    except Exception as e:
                        exceptions = json.load(open("Exceptions/reading.json", "r"))
                        exceptions["questions"].append([f"{examid[0]}-{pid[0]}-{question[0]}", f"{e}"])
                        json.dump(exceptions, open("Exceptions/reading.json", "w"))
                        cur.execute(
                            "UPDATE tpo.xdf.reading SET parsed = false WHERE examid = %s and pid = %s and question_index = %s",
                            (str(int(examid[0])), str(int(pid[0])), str(int(question[0]))))
                        continue
                elif int(question[0]) == last_first:
                    try:
                        multi_select(html)
                        print(f"{examid[0]}-{pid[0]}-{question[0]}")
                    except Exception as e:
                        exceptions = json.load(open("Exceptions/reading.json", "r"))
                        exceptions["questions"].append([f"{examid[0]}-{pid[0]}-{question[0]}", f"{e}"])
                        json.dump(exceptions, open("Exceptions/reading.json", "w"))
                        cur.execute(
                            "UPDATE tpo.xdf.reading SET parsed = false WHERE examid = %s and pid = %s and question_index = %s",
                            (str(int(examid[0])), str(int(pid[0])), str(int(question[0]))))
                        continue
                else:
                    try:
                        normal_multiple_choice(html)
                        print(f"{examid[0]}-{pid[0]}-{question[0]}")
                    except Exception as e:
                        exceptions = json.load(open("Exceptions/reading.json", "r"))
                        exceptions["questions"].append([f"{examid[0]}-{pid[0]}-{question[0]}", f"{e}"])
                        json.dump(exceptions, open("Exceptions/reading.json", "w"))
                        cur.execute(
                            "UPDATE tpo.xdf.reading SET parsed = false WHERE examid = %s and pid = %s and question_index = %s",
                            (str(int(examid[0])), str(int(pid[0])), str(int(question[0]))))
                        continue

                conn.commit()
            except Exception as e:
                exceptions = json.load(open("Exceptions/reading.json", "r"))
                exceptions["SQL"].append([f"{examid[0]}-{pid[0]}-{question[0]}", f"{e}"])

conn.close()
