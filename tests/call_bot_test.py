import sys
#Pfad zum Skript fuer das Versenden einfuegen
sys.path.append('/root/wm66_brew/tests')
import bot_sending_test

message = "Die WM66 braucht dich! Genug geschraubt an sozialistischen Schwestern Katzenhäusern!!! Auf auf!"
bot_sending_test.sendMsg(message)
