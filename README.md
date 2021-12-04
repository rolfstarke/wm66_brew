
setup pi
setup wm1thermsensor

#setup influxdb and grafana
https://www.circuits.dk/temperature-logger-running-on-raspberry-pi/

connect to VEBWaschgeraetewerk1
pw: schwarz3nb3rg


ssh pi@10.3.141.1

tmux new -s [name]
#prefix = ctrl + b
#prefic + c = new window
#prefix + [number] = window[number]
#prefix + % = split screen
#prefix + left = switch to left pane
#prefix + right = switch to right pane
#exit = close window
#prefix + d = detach session
#tmux ls = list sessions
#tmux attach -t [name]
#tmux kill-session -t [name] = delete session

#hier ist der alte stuff
cd ~
cd wm66_brew/
python3 brew.pytmux ls

#hier ist das repository
/home/pi/wm66_brew

https://github.com/rolfstarke/wm66_brew


git push https://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@github.com/rolfstarke/wm66_brew.git
