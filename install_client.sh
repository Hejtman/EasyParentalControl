#!/bin/sh

AUTOSTART=/etc/xdg/lxsession/LXDE-pi/autostart

echo "$(pwd)/client.py" >> ${AUTOSTART}
