from w1thermsensor import W1ThermSensor

def getTemp():

	temp = W1ThermSensor().get_temperature()
	return temp
