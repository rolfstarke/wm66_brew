import RPi.GPIO as GPIO
import time

# Konstanten für die Dauer der Agitation und die Verzögerung zwischen den Schüttelbewegungen
AGITATOR_DURATION = 0.1
DELAY_BETWEEN_SHAKES = 1

def shake(agitator_pin):
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
                print("Ungültige Eingabe. Bitte geben Sie eine ganze Zahl ein.")
        
        # Schleife für die angegebene Anzahl an Schüttelbewegungen durchlaufen
        counter = 0
        while counter < shakes:
            GPIO.output(agitator_pin, GPIO.HIGH)
            time.sleep(AGITATOR_DURATION)
            GPIO.output(agitator_pin, GPIO.LOW)
            counter += 1
            time.sleep(DELAY_BETWEEN_SHAKES)
            
        print("Agitation beendet ;-)")
    
    finally:
        # GPIO-Modus zurücksetzen und alle Pins freigeben
        GPIO.cleanup()
