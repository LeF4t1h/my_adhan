# my_adhan
Has a GUI branch and a no GUI branch.
This python script scrapes the current prayer times from namazvaktimi.com and plays and plays them when prayer time has come with a mp3 file.
The service that starts the python script is called **adhan.service**, which is under */etc/systemd/system/adhan.service*
The service that starts the script daily at 00:00 is called **adhan.timer**, which is under */etc/systemd/system/adhan.timer*
The service that stops adhan.service is a cronjob. The cronjob can only be seen with the sudo command however. It stops the service every night at 23:59.
The bluetooth device is connected on startup with **~/bt_auto_connect.sh** with the file **/etc/rc.local**

Useful commands:

`journalctl -u adhan.service` (press G to see the newest log entry)

`sudo systemctl status adhan.service`

`sudo systemctl status adhan.timer`

`sudo systemctl list-units --type=service --state=running`

`systemctl list-timers --all`

`sudo crontab -l`

`sudo nano /etc/systemd/system/adhan.service`

`sudo nano /etc/systemd/system/adhan.timer`

`sudo cat /etc/systemd/system/adhan.service`

`sudo cat /etc/systemd/system/adhan.timer`

`sudo reboot`

