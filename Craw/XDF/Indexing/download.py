import json
import os
import time

import psycopg2
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

data = json.load(open("index_info.json", 'r'))

load_dotenv()

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()


def craw(index: int):
    url = (f"https://www.testgts.com/toeflMockBrowse/mockWriteView?examId={index}&timuType=1&uid"
           f"=86bb44b21679490ebf8b9045447bc419&classExamId=191687")
    # time.sleep(3)
    try:
        resp = page.goto(url)
    except Exception:
        return None

    if resp.status == 200 and resp.text() != "":
        print(f"{index} is valid")
        indexes = page.query_selector("#sectionTabContent").inner_html()

        insert_sql = """INSERT INTO xdf.indexes (examid, indexes_html, extracted)
                        VALUES (%s, %s, DEFAULT);"""

        cur.execute(insert_sql, (index, indexes))
        conn.commit()

    else:
        print(f"{index} is invalid")
        data["fail"].append(index)
        return None

    data["success"].append(index)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto('https://passport.testgts.com/preLogin?gotoURL=https://www.testgts.com')
    page.wait_for_load_state('networkidle')

    page.fill('input[name="telemail"]', os.getenv("UNAME"))
    page.fill('input[name="password"]', os.getenv("PASSWORD"))

    page.click('button[type="submit"]')

    page.wait_for_load_state('networkidle')
    time.sleep(3)

    while data["curr_idx"] <= 1300:
        page.wait_for_load_state('networkidle')
        craw(data["curr_idx"])
        data["curr_idx"] += 1
        json.dump(data, open("index_info.json", 'w'))
        data = json.load(open("index_info.json", 'r'))

conn.close()
