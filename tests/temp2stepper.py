import RPi.GPIO as GPIO
import time
import datetime
from influxdb import InfluxDBClient
from w1thermsensor import W1ThermSensor
import w1thermsensor 

# Pins des ULN2003A-Treibers am Raspberry Pi
coil_A_1_pin = 17
coil_A_2_pin = 22
coil_B_1_pin = 23
coil_B_2_pin = 27

# Verzögerung zwischen den Schritten in Sekunden
step_delay = 0.01

# Steps pro Grad Celsius
steps_celsius = 40

# Startwert für last_output_value
last_output_value = 20

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set up GPIO pins for ULN2003A
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

# ULN2003A Schrittmuster in der richtigen Reihenfolge
step_sequence = [[0, 1, 0, 0],
                 [0, 1, 0, 1],
                 [0, 0, 0, 1],
                 [1, 0, 0, 1],
                 [1, 0, 0, 0],
                 [1, 0, 1, 0],
                 [0, 0, 1, 0],
                 [0, 1, 1, 0]]

# Funktion zum Setzen der ULN2003A-Schritte
def set_step(step):
    GPIO.output(coil_A_1_pin, step[0])
    GPIO.output(coil_A_2_pin, step[1])
    GPIO.output(coil_B_1_pin, step[2])
    GPIO.output(coil_B_2_pin, step[3])

# Funktion zum Abrufen der Temperatur
def get_temp():
	try:
		temp = W1ThermSensor().get_temperature()
		return temp
	
	# Ab und zu wird diese exception geworfen. Kein Plan warum...
	except w1thermsensor.errors.SensorNotReadyError:
		temp = None

try:
    while True:
        temperature = get_temp()

        # Wenn es mindestens einen Wert gibt, gebe den letzten Wert aus
        if temperature is not None:
            last_value = temperature
            rounded_value = round(last_value, 1)

            # Differenz zwischen den beiden Werten berechnen
            diff = rounded_value - last_output_value

            # Anzahl der Schritte berechnen
            steps = int(abs(diff) * steps_celsius)

            # Zeitstempel festlegen
            dt = "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())

            # Schritte in der entsprechenden Richtung ausführen
            if diff < 0:
                for i in range(steps):
                    for step in step_sequence:
                        set_step(step)
                        time.sleep(step_delay)
                print(f'{dt} | CCW: {steps} Schritte ausgeführt. Letzter Wert {rounded_value}')
            elif diff > 0:
                for i in range(steps):
                    for step in reversed(step_sequence):
                        set_step(step)
                        time.sleep(step_delay)
                print(f'{dt} | CW: {steps} Schritte ausgeführt. Letzter Wert {rounded_value}')
            else:
                print(f'{dt} | Keine Änderung des Wertes. Letzter Wert {rounded_value}')
                time.sleep(0.5)

            # Letzten Ausgabewert aktualisieren
            last_output_value = rounded_value

        else:
            print('Es gibt keine Werte in der Datenreihe.')

        # Wartezeit bis zur nächsten Abfrage
        # time.sleep(1)

except KeyboardInterrupt:
    print('Abbruch durch Nutzer')

except Exception as e:
    print(e)

finally:
    GPIO.cleanup()
