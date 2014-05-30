#!/bin/sh
DIR=$(dirname $0)
irc3 --logdir logs/ config.ini & disown
echo $! > idlebot.pid
