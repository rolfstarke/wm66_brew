# Hier die Optionsabfrage und starten der Subscripte
import sys
import getopt

import bot_send

# muss irgendwie sein...
argumentList = sys.argv[1:]
# Options
options = "bmw"
# Long Options
long_options = ["Bot", "Mash", "Wort"]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-b", "--Bot"):
            import bot_listen
             
        elif currentArgument in ("-m", "--Mash"):
            import mash
             
        elif currentArgument in ("-w", "--Wort"):
            import wort
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
