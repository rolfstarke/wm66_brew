import RPi.GPIO as GPIO
import time

def shake(agitator_pin, agitator_duration = 0.06, delay_between_shakes = 0.3):
    try:
        # GPIO-Modus auf BOARD setzen und den angegebenen Pin als Ausgang konfigurieren
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(agitator_pin, GPIO.OUT)
        
        # Benutzerabfrage für die Anzahl der Schüttelbewegungen
        while True:
            shakes_input = input("Wie oft soll die Agitation durchgeführt werden? ")
            try:
                shakes = int(shakes_input)
                break
            except ValueError:
                print("Depp. Gib eine ganze Zahl ein!")
        
        # Schleife für die angegebene Anzahl an Schüttelbewegungen durchlaufen
        counter = 0
        while counter < shakes:
            GPIO.output(agitator_pin, GPIO.HIGH)
            time.sleep(agitator_duration)
            GPIO.output(agitator_pin, GPIO.LOW)
            counter += 1
            time.sleep(delay_between_shakes)
            
        print("Agitation beendet ;-)")
    
    finally:
        # GPIO-Modus zurücksetzen und alle Pins freigeben
        GPIO.cleanup()
