#!/bin/bash

modprobe -r b43
modprobe -r brcmsmac
modprobe -r wl

modprobe wl
lsmod |grep 'brcmsmac\|b43\|wl'
