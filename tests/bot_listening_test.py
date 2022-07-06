import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
import Adafruit_DHT

def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        print('Got command: %s' % command)

        if command == '/temperatur':
                humidity, temperature = Adafruit_DHT.read(Adafruit_DHT.DHT22, 4)
                bot.sendMessage(chat_id, str(temperature))
#        elif command == '/zeit':
#               bot.sendMessage(chat_id, str(datetime.datetime.now()))
        elif command == '/spruch':
                with open('spruch_db.txt') as file:
                        sprueche = file.read().splitlines()
                g = len(sprueche)-1
                n = random.randint(0,g)
                bot.sendMessage(chat_id, str(sprueche[n]))

with open("../data/token.txt") as file:
        token = file.read().splitlines()

bot = telepot.Bot(token[0])

MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)
