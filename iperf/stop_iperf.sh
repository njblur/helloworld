#! /bin/bash
devices=`adb devices 2>/dev/null|grep -v List | awk '{print $1}'` 
for device in $devices
do
echo $device
perf=`adb -s $device shell ps iperf2_0_4 |awk '{print $2}'|grep -v PID`
echo $perf
adb -s $device shell kill $perf
done

