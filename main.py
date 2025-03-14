import sys
import subprocess
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import vlc
import os
import requests
import time
import signal


PRAYERS = ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"]
LINK = "https://www.namaztakvimi.com/almanya/bensheim-ezan-vakti.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}



def terminate_script(signum, frame):
    print("Adhan Clock stopped.")
    sys.exit(0)

signal.signal(signal.SIGTERM, terminate_script)



def get_prayer_times():
    """Scrapes today's prayer times and returns them in an array"""

    try:
        with requests.get(LINK, headers=headers) as response:
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            prayer_text = soup.find_all("h3", class_="mb-0 mt-4")
            times = [prayer.text for prayer in prayer_text]
            prayer_times = dict(zip(PRAYERS, times))

            if response.status_code != 200:
                print(f"Error, status code: {response.status_code}")
                exit()
            print(f"Scraped prayer times for {datetime.now()}: {prayer_times}")

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


def check_pulseaudio():
    # Check if PulseAudio is running
    try:
        subprocess.run(["pulseaudio", "--check"], check=True)
        print("PulseAudio is already running.")
    except subprocess.CalledProcessError:
        print("PulseAudio is not running, starting it now...")
        # Start PulseAudio
        subprocess.run(["pulseaudio", "--start"])
        time.sleep(2)  # Give PulseAudio time to start
        print("PulseAudio started.")


if __name__ == "__main__":
    check_pulseaudio() # comment out if on windows
    file_name = "Adhan-Turkish.mp3"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, file_name)
    player = vlc.MediaPlayer(file_path)
    adhan_times = get_prayer_times()
    
    # when starting the prayer for the first time, wait until it is exactly HH:00
    now = datetime.now()
    seconds_to_wait = 60 - now.second
    time.sleep(seconds_to_wait)
    
    while True:
        check_prayer_time()
        time.sleep(60)  # sleep 60 seconds -> check prayer time every minute

