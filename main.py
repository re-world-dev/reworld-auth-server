
import os
os.system("pip install -r requirements.txt")

version = "0.1"

#===============
#  RE:WORLD
#===============
#Import libs
from libs import console 
from libs import network 
import socket as skt
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
        console.alert("Please updade for to avoid exploit/server hacking !")
        console.alert("----------------")
        time.sleep(0.5)

except requests.exceptions.RequestException as e:
    console.alert(f"Failed to check updade error : {e}")

except Exception as e:
    console.alert(f"ERROR OCCURED : {e}")



console.info("Starting")

class AuthServer(object):
    def __init__(self):
        self.skt = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.skt.bind(("0.0.0.0", 9606))
        self.skt.listen(5)

    def start(self):
        while True:
            addr, info = self.skt.accept()
            msg = addr.recv(1024).decode().split("-")
            if msg[0] == "\x00":
                #Account creation
                if self.exists(msg[1]):
                    addr.send(b"\x00-0-This username is already taken !", 1024)
                    addr.close()
                    continue
                else:
                    self.add_account(username=msg[1], password=msg[2])
                    addr.send(b"\x01", 1024)
                    addr.close()
                    continue
            elif msg[0] == "\x01":
                #login
                if self.exists(msg[1]):
                    if self.check_password(msg[2]):
                        addr.send(b"\x01")
                    else:
                        addr.send(b"\x00-2-Username or password incorrect.")
                else:
                    addr.send(b"\x00-2-Username or password incorrect.")
                addr.close()
                continue

    def exists(self, user:str):
        """Search the database for a selected user. Return boolean"""
        exists = False
        for player in self._read():
            if player[0] == user and not(exists):
                exists = True
            elif player[0] == user and exists:
                raise InternalException(f"Two players with the same username were found. Username : {user}.")
            else:
                continue
        return exists
    
    def check_password(self, user:str, password:str):
        """Check the password of a specified user. Return a boolean"""
        user_data = self._get_user_by_name(user)
        if user_data["password"] == password:
            return True
        else:
            return False

    def _get_user_by_name(self, username:str):
        data = self._read()
        occ = []
        for player in data:
            if player["username"] == username:
                occ.append(player)
                continue
            else:
                continue
        if len(occ) > 1 :
            raise InternalException(f"More than one players with the username \"{username}\" were found !")
        elif len(occ) == 0:
            return None
        else:
            return occ[0]

    
    def _write(self, data:list):
        """# READ ME !!!!!!
        BE CAREFUL WITH THIS METHOD : IT JUST CLEAR THE OLD DATA. To modify you can get the old data with AuthServer._read() and modify the given data, then use this method."""
        with open("database.rewasdb", "w") as db:
            for line in data:
                db.writelines(f"{line['username']}\x00{line['password']}")

    def add_account(self, username:str, password:str):
        """Add a new account to the database"""
        dt = self._read()
        dt.append({"username": username, "password": password})
        self._write(dt)

    def _read(self):
        with open("database.rewasdb", "r") as db:
            data = db.read()
        peruserinfo = data.split("\n")
        database_content = []

        for player_infos in peruserinfo:
            username, password = player_infos.split("\x00")
            database_content.append({"username": username, "password": password})
            #maybe a day will come where we will add ranks or accounts types

        return database_content

class InternalException(object):
    pass

asrv = AuthServer()
asrv.start()