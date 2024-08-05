from monitors.janestreet import janestreet_monitor
from monitors.roblox import roblox_monitor
from monitors.databricks import databricks_monitor
from monitors.ramp import ramp_monitor
from monitors.modal import modal_monitor
from monitors.figma import figma_monitor
from monitors.robinhood import robinhood_monitor
import time

while True:
    try:
        janestreet_monitor()
        roblox_monitor()
        databricks_monitor()
        ramp_monitor()
        modal_monitor()
        figma_monitor()
        robinhood_monitor()
    except:
        print("Error in main.py")

    time.sleep(60)
