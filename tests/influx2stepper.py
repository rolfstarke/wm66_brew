import RPi.GPIO as GPIO
import time
from influxdb import InfluxDBClient

# Pins des ULN2003A-Treibers am Raspberry Pi
coil_A_1_pin = 17
coil_A_2_pin = 22
coil_B_1_pin = 4
coil_B_2_pin = 27

# Schritte pro Umdrehung des 28BYJ-48 Motors
steps_per_revolution = 512

# Verzögerung zwischen den Schritten in Sekunden
step_delay = 0.01

# Verbindung zur InfluxDB herstellen
client = InfluxDBClient(host='192.168.188.36', port=8086, username='grafana', password='12TUDdd.47', database='dhtTest')

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

last_output_value = 20

try:
    while True:
        # InfluxQL-Abfrage für den letzten Wert der Datenreihe
        query = 'SELECT last("temperature") FROM "TemperatureSensor"'

        # Abfrage an die InfluxDB senden
        result = client.query(query)

        # Ergebnis als Liste von Dictionaries abrufen
        points = list(result.get_points())

        # Wenn es mindestens einen Wert gibt, gebe den letzten Wert aus
        if points:
            last_value = points[0]['last']
            rounded_value = round(last_value, 1)

            # Differenz zwischen den beiden Werten berechnen
            diff = rounded_value - last_output_value

            # Anzahl der Schritte berechnen (20 Schritte pro Einheit Differenz)
            steps = int(abs(diff) * 40)

            # Schritte in der entsprechenden Richtung ausführen
            if diff < 0:
                for i in range(steps):
                    for step in step_sequence:
                        set_step(step)
                        time.sleep(step_delay)
                print(f'Uhrzeigersinn: {steps} Schritte ausgeführt. Letzter Wert {rounded_value}')
            elif diff > 0:
                for i in range(steps):
                    for step in reversed(step_sequence):
                        set_step(step)
                        time.sleep(step_delay)
                print(f'Gegen den Uhrzeigersinn: {steps} Schritte ausgeführt. Letzter Wert {rounded_value}')
            else:
                print(f'Keine Änderung des Wertes. Letzter Wert {rounded_value}')

            # Letzten Ausgabewert aktualisieren
            last_output_value = rounded_value

        else:
            print('Es gibt keine Werte in der Datenreihe.')

        # Wartezeit bis zur nächsten Abfrage
        time.sleep(60)

except KeyboardInterrupt:
    print('Abbruch durch Nutzer')

finally:
    GPIO.cleanup()
