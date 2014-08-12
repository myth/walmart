#!/bin/bash

modprobe -r b43
modprobe -r brcmsmac
modprobe -r wl

modprobe brcmsmac
lsmod |grep brcmsmac
