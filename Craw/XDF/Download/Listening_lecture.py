import copy
import os
import time
from urllib.parse import urlparse, parse_qs

import dotenv
import psycopg2
from bs4 import BeautifulSoup as bs
from playwright.sync_api import sync_playwright

dotenv.load_dotenv()

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    dbname="tpo",
    user="",
    password=""
)
cur = conn.cursor()
cur.execute("SELECT * FROM tpo.xdf.listening_lecture WHERE downloaded = false OR downloaded IS NULL")
rows = cur.fetchall()


def craw(url):
    try:
        idx = parse_qs(urlparse(url).query)['orderNum'][0]
    except Exception as e:
        # file = json.load(open("exceptions.json", 'r'))
        # file["reading"].append({"url": url, "exception": str(e)})
        # json.dump(file, open("exceptions.json", 'w'))
        idx = None
    page.goto(url)
    html = bs(page.content()).prettify()
    cur.execute(
        "UPDATE tpo.xdf.listening_lecture SET question_index = %s, full_html = %s, downloaded=true WHERE url = %s",
        (idx, html, url))
    print(f"examid: {parse_qs(urlparse(url).query)['examId'][0]}, idx: {idx}, successful")
    conn.commit()


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

    rows = copy.deepcopy(rows)
    for row in rows:
        craw(row[0])

conn.close()