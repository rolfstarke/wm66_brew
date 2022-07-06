import sys
#Pfad zum Skript fuer das Versenden einfuegen
sys.path.append('/home/pi/wm66_brew/tests')
import bot_sending_test

message = "26 C"
bot_sending_test.sendMsg(message)
