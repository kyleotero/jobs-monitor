from monitors.janestreet import janestreet_monitor
from monitors.roblox import roblox_monitor
from monitors.databricks import databricks_monitor
from monitors.ramp import ramp_monitor
from monitors.modal import modal_monitor
import time

while True:
    janestreet_monitor()
    roblox_monitor()
    databricks_monitor()
    ramp_monitor()
    modal_monitor()

    time.sleep(60)
