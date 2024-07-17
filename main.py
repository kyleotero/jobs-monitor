from monitors.janestreet import janestreet_monitor
from monitors.roblox import roblox_monitor
from monitors.databricks import databricks_monitor
import time

while True:
    janestreet_monitor()
    roblox_monitor()
    databricks_monitor()

    time.sleep(60)
