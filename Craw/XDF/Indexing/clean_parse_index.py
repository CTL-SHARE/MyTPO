import json

import psycopg2
from bs4 import BeautifulSoup as bs

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()
cur.execute("SELECT examid, indexes_html, extracted FROM tpo.xdf.indexes")
rows: list[tuple[int, str, bool]] = cur.fetchall()

exceptions: dict = json.loads("{}")

for row in rows:
    examid = row[0]
    indexes_html = row[1]
    indexes_html = bs(indexes_html).prettify()
    extracted = row[2]

    soup = bs(indexes_html, 'html.parser')
    sections = soup.find_all('div', {'class': 'row content-bottom'})

    try:
        # reading
        reading = sections[0].find_all('div', {'class': 'exam'})  # 2~3 parts
        for part in reading:
            questions = part.find_all('li')
            for j in questions:
                url = "https://www.testgts.com" + j['data-url'].replace('&amp;', '&')
                # print(url)
                insert_sql = """INSERT INTO tpo.xdf.reading (url, examid) VALUES (%s, %s)"""
                cur.execute(insert_sql, (url, examid,))

        # listening
        listening = sections[1].find_all('div', {'class': 'exam'})
        # mixed conversations and lectures, split using number of questions
        for part in listening:
            questions = part.find_all('li')
            if len(questions) == 5:  # conversation
                for i in questions:
                    url = "https://www.testgts.com" + i['data-url'].replace('&amp;', '&')
                    # print(url)
                    insert_sql = """INSERT INTO tpo.xdf.listening_conversation (url, examid) VALUES (%s, %s)"""
                    cur.execute(insert_sql, (url, examid,))
            elif len(questions) == 6:  # lecture
                for i in questions:
                    url = "https://www.testgts.com" + i['data-url'].replace('&amp;', '&')
                    # print(url)
                    insert_sql = """INSERT INTO tpo.xdf.listening_lecture (url, examid) VALUES (%s, %s)"""
                    cur.execute(insert_sql, (url, examid,))
            else:
                raise Warning(f"Error number of **listening** questions with ```\n {part} \n``` in exam {examid}")

        # speaking
        speaking = sections[2].find('div', {'class': 'exam'}).find_all('li')  # only 1 exam tag inside
        if len(speaking) == 4:  # new TOEFL
            q1 = "https://www.testgts.com" + speaking[0]['data-url'].replace('&amp;', '&')
            q1_insert_sql = """INSERT INTO tpo.xdf.speaking_q1 (url, examid) VALUES (%s, %s)"""
            cur.execute(q1_insert_sql, (q1, examid,))

            q2 = "https://www.testgts.com" + speaking[1]['data-url'].replace('&amp;', '&')
            q2_insert_sql = """INSERT INTO tpo.xdf.speaking_q2 (url, examid) VALUES (%s, %s)"""
            cur.execute(q2_insert_sql, (q2, examid,))

            q3 = "https://www.testgts.com" + speaking[2]['data-url'].replace('&amp;', '&')
            q3_insert_sql = """INSERT INTO tpo.xdf.speaking_q3 (url, examid) VALUES (%s, %s)"""
            cur.execute(q3_insert_sql, (q3, examid,))

            q4 = "https://www.testgts.com" + speaking[3]['data-url'].replace('&amp;', '&')
            q4_insert_sql = """INSERT INTO tpo.xdf.speaking_q4 (url, examid) VALUES (%s, %s)"""
            cur.execute(q4_insert_sql, (q4, examid,))

            # print(q1, q2, q3, q4)
        elif len(speaking) == 6:  # old TOEFL
            q1 = "https://www.testgts.com" + speaking[1]['data-url'].replace('&amp;', '&')
            q1_insert_sql = """INSERT INTO tpo.xdf.speaking_q1 (url, examid) VALUES (%s, %s)"""
            cur.execute(q1_insert_sql, (q1, examid,))

            q2 = "https://www.testgts.com" + speaking[2]['data-url'].replace('&amp;', '&')
            q2_insert_sql = """INSERT INTO tpo.xdf.speaking_q2 (url, examid) VALUES (%s, %s)"""
            cur.execute(q2_insert_sql, (q2, examid,))

            q3 = "https://www.testgts.com" + speaking[3]['data-url'].replace('&amp;', '&')
            q3_insert_sql = """INSERT INTO tpo.xdf.speaking_q3 (url, examid) VALUES (%s, %s)"""
            cur.execute(q3_insert_sql, (q3, examid,))

            q4 = "https://www.testgts.com" + speaking[5]['data-url'].replace('&amp;', '&')
            q4_insert_sql = """INSERT INTO tpo.xdf.speaking_q4 (url, examid) VALUES (%s, %s)"""
            cur.execute(q4_insert_sql, (q4, examid,))

            # print(q1, q2, q3, q4)
        else:
            raise Warning(f"Error number of **speaking** questions with ```\n {speaking} \n``` in exam {examid}")

        # writing
        writing = sections[3].find('div', {'class': 'exam'}).find_all('li')  # only 1 exam tag inside
        if len(writing) != 2:
            raise Warning(f"Error number of **writing** questions with ```\n {writing} \n``` in exam {examid}")
        else:
            integrated = "https://www.testgts.com" + writing[0]['data-url'].replace('&amp;', '&')
            # print(integrated)
            integrated_insert_sql = """INSERT INTO tpo.xdf.writing_integrated (url, examid) VALUES (%s, %s)"""
            cur.execute(integrated_insert_sql, (integrated, examid,))

            independent = "https://www.testgts.com" + writing[1]['data-url'].replace('&amp;', '&')
            # print(independent)
            independent_insert_sql = """INSERT INTO tpo.xdf.writing_independent (url, examid) VALUES (%s, %s)"""
            cur.execute(independent_insert_sql, (independent, examid,))

    except Exception as e:
        exceptions[str(examid)] = str(e)
        print(f"{examid} has errors")
        update_sql = """UPDATE tpo.xdf.indexes SET indexes_html = %s WHERE examid = %s"""
        cur.execute(update_sql, (indexes_html, examid,))
        continue

    update_sql = """UPDATE tpo.xdf.indexes SET extracted = true, indexes_html = %s WHERE examid = %s"""
    cur.execute(update_sql, (indexes_html, examid,))

    print(f"{examid} completes successfully")

exceptions_file = open("exceptions.json", 'w')
json.dump(exceptions, exceptions_file)

conn.commit()
cur.close()
conn.close()
