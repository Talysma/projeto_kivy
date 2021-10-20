#!/bin/sh
adb logcat | grep -F "`adb shell ps | grep br.pro.just.redesocial  | tr -s [:space:] ' ' | cut -d' ' -f2`"
