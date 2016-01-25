#!/bin/bash
# This script tests usage of loadYoyoData.py

echo "./loadYoyoData.py"
./loadYoyoData.py 1> silent_stdout
if [[ $? == 0 ]];then
   echo "PASS"
else
   echo "FAIL"
fi
./loadYoyoData.py /media/usb 1>> silent_stdout
echo "./loadYoyoData.py /media/usb"
if [[ $? == 0 ]];then
   echo "PASS"
else
   echo "FAIL"
fi
./loadYoyoData.py /media/usb/Input 1>> silent_stdout
echo "./loadYoyoData.py /media/usb/Input"
if [[ $? == 0 ]];then
   echo "PASS"
else
   echo "FAIL"
fi
