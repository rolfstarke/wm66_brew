import requests

def sendMsg(msg):
    #Pfad zum Token einfügen    
    with open("data/token.txt") as file:
        token = file.read().splitlines()
    url = f"https://api.telegram.org/bot{token[0]}/sendMessage"
    params = {"chat_id":"-792733418", "text":msg}
    try:
        message = requests.post(url, params=params)
    except:
	    pass
