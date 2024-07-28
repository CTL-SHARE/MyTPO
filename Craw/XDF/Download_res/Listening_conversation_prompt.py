import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
import requests

conn = psycopg2.connect(host="localhost", port="5432", dbname="tpo", user="", password="")
cur = conn.cursor()
cur.execute(
    "SELECT DISTINCT examid, audioid, num, prompt_audio_url FROM tpo.xdf.listening_conversation WHERE prompt_audio_download is null ORDER BY examid, audioid")
rows = cur.fetchall()

download_dir = '/Users/Taylor/Desktop/MyTPO/Craw/XDF/Download_res/res/Listening_conversation_prompt'
os.makedirs(download_dir, exist_ok=True)

user_agent = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def download_file(row):
    examid, audioid, num, listening_audio_url = row
    local_filename = f"{str(int(examid))}-{str(int(audioid))}-{str(int(num))}.mp3"
    audio_url = listening_audio_url.replace('{', '').replace('}', '').replace('\"', '')
    file_path = os.path.join(download_dir, local_filename)
    try:
        with requests.get(audio_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        cur.execute(
            "UPDATE tpo.xdf.listening_conversation SET prompt_audio_local_name = %s, prompt_audio_download = true WHERE prompt_audio_url = %s",
            (local_filename, listening_audio_url))
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
