import sys
#Pfad zum Skript fuer das Versenden einfuegen
sys.path.append('/home/pi/wm66_brew/tests')
import bot_test2

message = "26 C"
bot_test2.sendMsg(message)
