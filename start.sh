#!/bin/bash
python3 bot_listen.py > /dev/null 2>1& &
echo Bot hoert zu
python3 brew.py
