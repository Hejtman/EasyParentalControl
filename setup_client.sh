#!/bin/sh

AUTOSTART=/etc/xdg/lxsession/LXDE/autostart

echo "$(pwd)/client.py" >> ${AUTOSTART}
