import sys
#Pfad zum Skript fuer das Versenden einfuegen
sys.path.append('/root/wm66_brew/tests')
import bot_sending_test

message = "Rolf! Rede mit mir!"
bot_sending_test.sendMsg(message)
