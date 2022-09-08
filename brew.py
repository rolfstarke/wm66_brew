import sys
import getopt

import bot_send

# muss irgendwie sein...
argumentList = sys.argv[1:]
# Options
options = "tmwch"
# Long Options
long_options = ["Telegram", "Mash", "Wort", "Cool", "Help"]

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-t", "--Telegram"):
            bot_send.sendMsg("Ich hoere zu.")
            subprocess.call("bot_listen.py", Shell=False)
             
        elif currentArgument in ("-m", "--Mash"):
            bot_send.sendMsg("Es wird eingemaischt!")
            subprocess.call("mash.py", Shell=True)
             
        elif currentArgument in ("-w", "--Wort"):
            bot_send.sendMsg("Würzekochen!")
            subprocess.call("wort.py", Shell=True)
            
        elif currentArgument in ("-c", "--Cool"):
            bot_send.sendMsg("Jetzt wird abgekuehlt!")
            subprocess.call("cool.py", Shell=True)
            
        elif currentArgument in ("-h", "--Help"):
            print("Erklärung... Filler bla bla bla")
             
except getopt.error as err:
    # output error, and return with an error code
    print(str(err))
