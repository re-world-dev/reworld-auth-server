
import os
os.system("pip install -r requirements.txt")

version = "0.1"

#===============
#  RE:WORLD
#===============
#Import libs
from libs import console 
from libs import network 
import socket
import time
import requests


console.info("-----------------------------")
console.info("RE:WORLD")
console.info("2023 The RE:WORLD project")
console.info("-----------------------------")
console.info("Discord : https://discord.gg/EauquJY6aQ")
time.sleep(2)
console.info("Checking for uptade...")


try:
    response = requests.get("SERVER")
    response.raise_for_status()
    page = response.text.strip()

    if page == version:
        console.info("This server software is up to date !")
    else:
        console.alert("----------------")
        console.alert('Version avaiable')
        console.alert("Please uptade for to avoid exploit/server hacking !")
        console.alert("----------------")
        time.sleep(0.5)

except requests.exceptions.RequestException as e:
    console.alert(f"Failed to check uptade error : {e}")

except Exception as e:
    console.alert(f"ERROR OCCURED : {e}")



console.info("Starting SOCKET")