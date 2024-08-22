import vlc
import time
import os

CWD = os.getcwd()
player = vlc.MediaPlayer(os.path.join(CWD, "Adhan-Turkish.mp3"))

print("Starting playback...")
player.play()
time.sleep(1)
while player.is_playing():
        time.sleep(0.1)
print("Playback finished.")
player.stop()

