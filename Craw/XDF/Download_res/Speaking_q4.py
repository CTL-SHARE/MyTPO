import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
import requests

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()
cur.execute("SELECT url, examid, audio_url FROM tpo.xdf.speaking_q4 WHERE audio_download = false ORDER BY examid")
rows = cur.fetchall()

download_dir = '/Users/Taylor/Desktop/MyTPO/Craw/XDF/Download_res/res/Speaking_q4'
os.makedirs(download_dir, exist_ok=True)

user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def download_file(row):
    url, examid, audio_url = row
    local_filename = str(examid) + ".mp3"
    audio_url = audio_url.replace('{', '').replace('}', '').replace('\"', '')
    file_path = os.path.join(download_dir, local_filename)
    try:
        with requests.get(audio_url, stream=True, headers=user_agent) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        cur.execute("UPDATE tpo.xdf.speaking_q4 SET audio_local_name = %s, audio_download = true WHERE url = %s",
                    (local_filename, url))
        conn.commit()
        return local_filename
    except Exception as e:
        return f"Error downloading {audio_url}: {e}"


def download_all_files(rows):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_file, row) for row in rows]
        for future in as_completed(futures):
            result = future.result()
            if "Error" not in result:
                print(f"Downloaded and saved {result}")
            else:
                print(result)


download_all_files(rows)

cur.close()
conn.close()
