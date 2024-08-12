from bs4 import BeautifulSoup
import tkinter as tk
from datetime import datetime, timedelta
import vlc
import platform
import os
import requests

if platform.system() == "Linux":
    from VolumeControllerLinux import *
elif platform.system() == "Windows":
    from VolumeControllerWindows import *

PRAYERS = ["İmsak", "Güneş", "Öğle", "İkindi", "Akşam", "Yatsı"]
CWD = os.getcwd()
TOMORROW = datetime.min
LINK = "https://www.namaztakvimi.com/almanya/bensheim-ezan-vakti.html"


def get_prayer_times():
    """Scrapes today's prayer times and returns them in an array"""

    try:
        response = requests.get(LINK)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        prayer_text = soup.find_all("h3", class_="mb-0 mt-4")
        times = []
        for i in range(len(prayer_text)):
            times.append(prayer_text[i].text)
        prayer_times = dict(zip(PRAYERS, times))

        return prayer_times
    finally:
        # Set tomorrow's date
        global TOMORROW
        tmp = datetime.now()
        TOMORROW = tmp.replace(
            day=tmp.day + 1, hour=0, minute=0, second=0, microsecond=0
        )


def get_current_time_interval(intervals):
    """calculate current interval"""
    now = datetime.now().strftime("%H:%M")

    # Iterate over each interval to find the current time interval
    for start_time, end_time in intervals:
        if start_time <= now < end_time:
            return start_time, end_time
        if end_time < start_time:
            # should be the only case where end_time < start_time -> midnight interval
            return start_time, end_time


def time_difference(start_time_str, end_time_str):
    """Calculate the difference between two times in 'HH:MM' format."""
    # Define time format
    time_format = "%H:%M"

    # Parse the time strings into datetime objects
    start_time = datetime.strptime(start_time_str, time_format)
    end_time = datetime.strptime(end_time_str, time_format)

    # Handle end time less than start time (spanning midnight)
    if end_time < start_time:
        end_time += timedelta(days=1)  # Add one day to end_time

    # Calculate the difference
    time_diff = end_time - start_time

    # Convert the difference to total minutes
    total_minutes = time_diff.total_seconds() / 60

    if total_minutes >= 60:
        hours = int(total_minutes // 60)
        remaining_minutes = int(total_minutes % 60)
        return f"{hours:02d}:{remaining_minutes:02d}"
    else:
        return f"{int(total_minutes)} minutes"


def update_prayer_times():
    """Updates the remaining time to the next prayer every minute. Also checks if it is necessary to update the
    prayer times if the next day has arrived"""

    # check if it is necessary to update the prayer times to the next day
    global TOMORROW
    if datetime.now() >= TOMORROW:
        global adhan_times
        adhan_times = get_prayer_times()

    # time intervals to highlight which time interval one currently is in
    time_intervals = []
    for i in range(len(PRAYERS)):
        # case yatsi and sabah namaz
        if i == len(PRAYERS) - 1:
            time_intervals.append(
                (adhan_times.get(PRAYERS[i]), adhan_times.get(PRAYERS[0]))
            )
        else:
            time_intervals.append(
                (adhan_times.get(PRAYERS[i]), adhan_times.get(PRAYERS[i + 1]))
            )

    # calculate the current prayer time interval
    current_interval = get_current_time_interval(time_intervals)

    # configure which prayer times should play the adhan
    if (
        (current_interval[0] == adhan_times.get(PRAYERS[2]))
        or (current_interval[0] == adhan_times.get(PRAYERS[3]))
        or (current_interval[0] == adhan_times.get(PRAYERS[4]))
    ):
        play_adhan(current_interval[0])

    i = 0
    # append the prayer times to the frame
    for prayer in adhan_times.keys():
        # text of current interval should be orange
        if current_interval[0] == adhan_times.get(prayer):
            label = tk.Label(root, text=prayer, fg="orange", font=("Arial", 16))
            adhan_label = tk.Label(
                root, text=adhan_times.get(prayer), fg="orange", font=("Arial", 16)
            )
        else:
            label = tk.Label(root, text=prayer, font=("Arial", 16))
            adhan_label = tk.Label(
                root, text=adhan_times.get(prayer), font=("Arial", 16)
            )
        label.grid(row=i, column=0, sticky="w", padx=8, pady=8)
        adhan_label.grid(row=i, column=1, sticky="e", padx=8, pady=8)
        i += 1

    # calculate the remaining time to the next prayer
    difference = time_difference(datetime.now().strftime("%H:%M"), current_interval[1])

    # append the remaining time to the frame
    diff_label = tk.Label(root, text=difference, fg="orange", font=("Arial", 16))
    diff_label.grid(row=7, column=0, sticky="nsew", padx=8, pady=8, columnspan=2)

    # print("Scheduling update_prayer_times()...")
    root.after(60000, update_prayer_times)


def play_adhan(interval_to_check):
    """Checks if it is time to play adhan"""

    now = datetime.now().strftime("%H:%M")
    if now == interval_to_check:
        player = vlc.MediaPlayer(os.path.join(CWD, "Adhan-Turkish.mp3"))
        player.play()


def __play_test():
    """private method to check the mp3 playing functionality"""
    player = vlc.MediaPlayer(os.path.join(CWD, "Adhan-Turkish.mp3"))
    player.play()


def update_button_text():
    """changes the image of the mute button"""
    if volume_controller.muted:
        mute_button.config(image=mute_image)
    else:
        mute_button.config(image=loud_image)


def on_mute_button_click():
    """function that gets called when the mute mutton is pressed"""
    volume_controller.toggle_mute()
    update_button_text()


if __name__ == "__main__":
    volume_controller = VolumeController()

    root = tk.Tk()
    root.title("Prayer Times")
    root.geometry("480x320")  # size of a raspberry pi touch display
    root.attributes("-fullscreen", True)

    loud_image = tk.PhotoImage(file=os.path.join(CWD, "loud_sound.png"))
    mute_image = tk.PhotoImage(file=os.path.join(CWD, "mute.png"))

    # Create a button and add it to the frame
    mute_button = tk.Button(root, image=loud_image, command=on_mute_button_click)
    mute_button.grid(row=0, column=2, padx=150, rowspan=7)

    # play_button = tk.Button(root, text="play", command=__play_test)
    # play_button.grid(row=0, column=3, padx=10, pady=10)

    adhan_times = get_prayer_times()
    update_prayer_times()

    root.mainloop()
