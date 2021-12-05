## Wm66 Brew

We turned the GDR washing machine "WM66" into an brewing kettle.

## Setup

[This](https://braumagazin.de/article/bierbrauen-mit-der-wm66-teil-1/) and [this](https://braumagazin.de/article/bierbrauen-mit-der-wm66-teil-2/) served as an inspiration, but we control the heating and the agitator of the wm66 via a relay with a raspberry pi 4.

the pi is flashed with Raspberry Pi OS Lite (64-bit)

[this](https://raspap.com/) is used to create an hotspot with the raspberry pi. In our case the SSH connection is established with:

```
ssh pi@10.3.141.1
```

[this](https://pimylifeup.com/raspberry-pi-influxdb/) is used to create a influxdb database

get pip.

```
sudo apt-get install python-pip
```

The temperature sensor DS18B20 is connected to the raspberry pi like [this](https://pimylifeup.com/raspberry-pi-temperature-sensor/) and implemented with the [wm1thermsensor](https://github.com/timofurrer/w1thermsensor) python module.

```
pip install w1thermsensor
```

https://pimylifeup.com/raspberry-pi-temperature-sensor/

wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.3-linux-arm64.deb

#setup influxdb and grafana
https://www.circuits.dk/temperature-logger-running-on-raspberry-pi/

connect to VEBWaschgeraetewerk1
pw: schwarz3nb3rg