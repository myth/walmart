#!/bin/bash

modprobe -r b44 b43 b43legacy ssb brcmsmac

modprobe wl
lsmod |grep 'brcmsmac\|b43\|wl'
