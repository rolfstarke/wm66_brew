import sys
#Pfad zum Skript fuer das Versenden einfuegen
sys.path.append('/root/wm66_brew/tests')
import bot_sending_test

message = "Hallo?!?!?! Roooooolf?!?!?" #input("Was denkt die WM66 gerade?")
bot_sending_test.sendMsg(message)
