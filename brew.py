# Hier die Optionsabfrage und starten der Subscripte
import sys
import getopt

import bot_send

# muss irgendwie sein...
argumentList = sys.argv[1:]
# Options
options = "tmw"
# Long Options
long_options = ["Telegram", "Mash", "Wort"]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-t", "--Telegram"):
            bot_send.sendMsg("Ich hoere zu.")
            import bot_listen
             
        elif currentArgument in ("-m", "--Mash"):
            bot_send.sendMsg("Es wird eingemaischt!")
            import mash
             
        elif currentArgument in ("-w", "--Wort"):
            bot_send.sendMsg("Würzekochen!")
            import wort
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
