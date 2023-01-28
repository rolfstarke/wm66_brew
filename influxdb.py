from influxdb import client as influxdb

def write(temp, target):
	influxMetric = [{
		'measurement': beer_name,
		'time': datetime.datetime.now(timezone('CET')),
		'fields': {'temperature': temp, 'target_temperature': target}
	}]

	influxHost = 'localhost'
	influxPort = '8086'
	influxUser = 'grafana'
	influxPasswd = 'ERZ2022WM66'
	influxdbName = 'brew_temperature'

	try:
		db = influxdb.InfluxDBClient(influxHost, influxPort, influxUser, influxPasswd, influxdbName)
		db.write_points(influxMetric)
	finally:
		db.close()
