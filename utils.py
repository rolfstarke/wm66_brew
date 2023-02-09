import requests
import time
import random
import datetime
#import telepot
#from telepot.loop import MessageLoop
#from w1thermsensor import W1ThermSensor

def testa():
    print("import test")

# temperatur abfragen

""" def current_temp():

    temperature = W1ThermSensor().get_temperature()
    return temperature

# influxdb schreiben

def writeInflux(temp, target, beer):
    influxMetric = [{
        'measurement': beer,
        'time': datetime.datetime.now(timezone('CET')),
        'fields': {'temperature': temp, 'target_temperature': target}
    }]

    influxHost = 'localhost'
    influxPort = '8086'
    influxUser = 'grafana'
    influxPasswd = 'ERZ2022WM66'
    influxdbName = 'brew_temperature'

    try:
        db = influxdb.InfluxDBClient(
            influxHost, influxPort, influxUser, influxPasswd, influxdbName)
        db.write_points(influxMetric)
    finally:
        db.close()

# heizungssteuerung


def heater_control(target_temp):

    if current_temp() < target_temp:
        GPIO.output(heater_pin, GPIO.HIGH)
        print("[" + str(datetime.datetime.now(timezone('CET'))) + "]" + " | current temperature: " +
              str(round(current_temp(), 1)) + " °C " + "| heater: on    ", end='\r')
        time.sleep(relay_interval)
    else:
        GPIO.output(heater_pin, GPIO.LOW)
        print("[" + str(datetime.datetime.now(timezone('CET'))) + "]" + " | current temperature: " +
              str(round(current_temp(), 1)) + " °C " + "| heater: idle    ", end='\r')
        time.sleep(relay_interval)




def sendMsg(msg):
    #Pfad zum Token einfügen    
    with open("data/token.txt") as file:
        token = file.read().splitlines()
    url = f"https://api.telegram.org/bot{token[0]}/sendMessage"
    params = {"chat_id":"-792733418", "text":msg}
    message = requests.post(url, params=params)



def handle(msg):
        chat_id = msg['chat']['id']
        command = msg['text']

        #print('Got command: %s' % command)

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
#print('I am listening ...')

while 1:
    time.sleep(10) """