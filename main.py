from monitors.janestreet import janestreet_monitor
import time

while True:
    janestreet_monitor()

    time.sleep(60)
