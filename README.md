## Wm66 Brew

We turned the GDR washing machine "WM66" into an brewing kettle.

## Setup

[This](https://braumagazin.de/article/bierbrauen-mit-der-wm66-teil-1/) and [this](https://braumagazin.de/article/bierbrauen-mit-der-wm66-teil-2/) served as an inspiration, but we control the heating and the agitator of the wm66 via a relay with a raspberry pi 4.

the pi is flashed with Raspberry Pi OS Lite (32-bit)

[this](https://www.elektronik-kompendium.de/sites/raspberry-pi/2002171.htm) is used to create an hotspot with the raspberry pi. In our case the SSH connection is established with:

```
ssh pi@192.168.1.1
```



[this](https://pimylifeup.com/raspberry-pi-influxdb/) is used to create a influxdb database

[this](https://simonhearne.com/2020/pi-influx-grafana/) as an example for influxdb database creation and user creation

get pip and git

```
sudo apt install git
sudo apt-get install python3-pip
```

The temperature sensor DS18B20 is connected to the raspberry pi like [this](https://pimylifeup.com/raspberry-pi-temperature-sensor/) and implemented with the [wm1thermsensor](https://github.com/timofurrer/w1thermsensor) python module.

```
pip3 install w1thermsensor
```

Enable 1-Wire in Interfacing Options in raspi-config


https://pimylifeup.com/raspberry-pi-temperature-sensor/

```
wget https://dl.influxdata.com/influxdb/releases/influxdb2-2.0.3-linux-arm64.deb
```

#setup influxdb and grafana
[this](https://www.circuits.dk/temperature-logger-running-on-raspberry-pi/)

connect to VEBWaschgeraetewerk1
pw: schwarz3nb3rg

#install tmux
```
sudo apt-get install tmux 
```
#relevant tmux commands
```
tmux ls
tmux new -s sessionname
tmux attach-session -t sessionname
```
#detach from session, shortcut
```
Ctrl + b d
```
#more tmux commands
[this](https://comtronic.com.au/blog/wp-content/uploads/comtronic_cheatsheet_tmux_A4.pdf)


