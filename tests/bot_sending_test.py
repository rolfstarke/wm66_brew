import requests
import json

def sendMsg(msg):
    #Pfad zum Token einfuegen    
    with open("../data/token.txt") as file:
        token = file.read().splitlines()
    url = f"https://api.telegram.org/bot{token[0]}/sendMessage"
    params = {"chat_id":"-1971489754", "text":msg}
    message = requests.post(url, params=params)
