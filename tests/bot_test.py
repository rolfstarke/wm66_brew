import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()
#print(args.echo)

with open("token.txt") as file:
        token = file.read().splitlines()
#urlA = f"https://api.telegram.org/bot{token[0]}/getUpdates"
#answer = requests.get(urlA)

#content = answer.content
#data = json.loads(content)
#print(data)

url = f"https://api.telegram.org/bot{token[0]}/sendMessage"
params = {"chat_id":"-792733418", "text":args.echo}
message = requests.post(url, params=params)
#print(message)