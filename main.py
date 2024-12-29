import sys

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import vlc
import os
import requests
import time
import signal


PRAYERS = ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"]
CWD = os.getcwd()
LINK = "https://www.namaztakvimi.com/almanya/bensheim-ezan-vakti.html"

def terminate_script(signum, frame):
    print("Adhan Clock stopped.")
    sys.exit(0)

signal.signal(signal.SIGTERM, terminate_script)


def get_prayer_times():
    """Scrapes today's prayer times and returns them in an array"""

    try:
        with requests.get(LINK) as response:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            prayer_text = soup.find_all("h3", class_="mb-0 mt-4")
            times = [prayer.text for prayer in prayer_text]
            prayer_times = dict(zip(PRAYERS, times))

            if response.status_code != 200:
                print(f"Error, status code: {response.status_code}")
            print(f"Scraped prayer times: {prayer_times}")

            return prayer_times
    except requests.exceptions.ConnectionError:
        print("Connection Error to", LINK)


def check_prayer_time():
    """Check if now is the prayer time. Comment in/out the prayers you want to hear."""

    times_to_check = [
        # adhan_times.get("İmsak"),
        adhan_times.get("Öğle"),
        adhan_times.get("İkindi"),
        adhan_times.get("Akşam"),
        adhan_times.get("Yatsı"),
    ]

    now = datetime.now().strftime("%H:%M")

    if now in times_to_check:
        play_adhan()


def play_adhan():
    """Plays the adhan mp3 when now == prayer time"""

    player.play()
    time.sleep(1)  # small delay before checking if playback has started
    while player.is_playing():
        time.sleep(0.1)
    player.stop()


if __name__ == "__main__":
    player = vlc.MediaPlayer(os.path.join(CWD, "Adhan-Turkish.mp3"))

    adhan_times = get_prayer_times()

    while True:
        check_prayer_time()
        time.sleep(60)  # sleep 60 seconds -> check prayer time every minute
