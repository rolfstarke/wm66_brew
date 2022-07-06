import requests
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("echo")
args = parser.parse_args()

with open("data/token.txt") as file:
        token = file.read().splitlines()

url = f"https://api.telegram.org/bot{token[0]}/sendMessage"
params = {"chat_id":"-792733418", "text":args.echo}
message = requests.post(url, params=params)