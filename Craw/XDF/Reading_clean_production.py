import re

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()

cur.execute(
    "SELECT prompt_clean, passage_clean, choices, url FROM tpo.xdf.reading where passage_json is null or prompt_json is null or choices_json is null or paragraph_num is null order by examid, pid, question_index")

rows = cur.fetchall()

for row in rows:
    prompt = bs(row[0], 'html.parser')
    prompt_json = []
    for i in prompt.find_all('p'):
        tmp = []
        for j in i.children:
            if j.name == 'span':
                tmp.append("@#" + j.get_text(strip=True))
            elif j.get_text(strip=True) != '':
                tmp.append(j.get_text(strip=True))
        if tmp:
            prompt_json.append(tmp)

    match = re.search(r'paragraph\s*(\d+)', prompt.get_text(strip=True))
    if match:
        paragraph_num = int(match.group(1))
    else:
        paragraph_num = -1

    passage = bs(row[1], 'html.parser')
    passage_json = [passage.find(re.compile('^h[1-6]$')).get_text(strip=True)]

    for i in passage.find_all('p'):
        tmp = []
        for j in i.children:
            if (j.name == 'span' or j.name == 'i') and (j.get_text(strip=True) != ''):
                tmp.append("@#" + j.get_text(strip=True))
            elif j.get_text(strip=True) != '':
                tmp.append(j.get_text(strip=True))
        if tmp:
            passage_json.append(tmp)

    choices = row[2]
    choices_json = []
    for i in choices:
        for x in ['A. ', 'B. ', 'C. ', 'D. ', 'E. ', 'F. ', 'G. ', 'H. ', 'I. ', 'J. ',
                  'A.', 'B.', 'C.', 'D.', 'E.', 'F.', 'G.', 'H.', 'I.', 'J.',
                  'A ', 'B ', 'C ', 'D ', 'E ', 'F ', 'G ', 'H ', 'I ', 'J ',
                  'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
            if i.startswith(x):
                i = i.replace(x, '')
                choices_json.append(i)
                break

    cur.execute(
        "UPDATE tpo.xdf.reading SET prompt_json = %s, passage_json = %s, choices_json = %s, paragraph_num = %s WHERE url = %s",
        (str(prompt_json), str(passage_json), str(choices_json), paragraph_num, row[3]))
    conn.commit()
