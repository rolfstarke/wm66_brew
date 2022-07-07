import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
from w1thermsensor import W1ThermSensor

def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        print('Got command: %s' % command)

        if command == '/temperatur':
                temperature = W1ThermSensor().get_temperature()
                bot.sendMessage(chat_id, str(round(temperature, 1)) + " °C ")
        elif command == '/spruch':
                with open('data/spruch_db.txt') as file:
                        sprueche = file.read().splitlines()
                g = len(sprueche)-1
                n = random.randint(0,g)
                bot.sendMessage(chat_id, str(sprueche[n]))

with open("data/token.txt") as file:
        token = file.read().splitlines()

bot = telepot.Bot(token[0])

MessageLoop(bot, handle).run_as_thread()
print('I am listening ...')

while 1:
    time.sleep(10)
