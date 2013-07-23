#!/bin/bash
#description: reboot the specified device for n times.
#author     : jianwu.hu@intel.com
usage() {
    echo >&1 "Usage: $0 [-s <device sn> ] [ -n reboot number ] [ -h ] "
    echo >&1 "       -s <device serial number>: default to first device by adb devices"
    echo >&1 "       -n <reboot number>:defaults to 1000"
    echo >&1 "       -h:                this help message"
    exit 1
}

device=`adb devices 2>/dev/null|grep -v List | awk '{print $1}' |head -1`
reboot_count=0
total=1000

if [ -z ${device} ]; then
    echo " no device connect, please connect your device to start the test"
    exit 1
fi
if [ $# -gt 0 ]
    then
    while getopts s:n:h opt
    do
        case "${opt}" in
        s )
            target_device=`adb devices 2>/dev/null|grep ${OPTARG} | awk '{print $1}'`
            if [ ${target_device} == ${OPTARG} ]; then
                device=$target_device
                else
                echo "could not find the device you specified,please try with correct serial no."
                exit 1
            fi
            ;;
        n )
            total=$((OPTARG+1-1))
            if [ $total -eq 0 ]; then
                echo "wrong reboot number!"
                usage
            fi
            ;;
        h )
            echo "found h option ${OPTARG}"
            usage
            ;;
        * )
            usage
        esac
    done
fi
sw_version=`adb -s ${device} shell getprop ro.build.fingerprint`
echo "found device: ${device},ready for reboot test"
echo "fingerprint: $sw_version"
begin_time=`adb -s ${device} shell date`
host_time=`date`
echo "test start at "
echo "mobile time: $begin_time"
echo "host time $host_time"
echo "total ${total} times"
while [ $((total--)) -gt 0 ] 
do
    adb shell sendevent /dev/input/event6 1 116  1; 
    adb shell sendevent /dev/input/event6 0 0 0; 
    sleep 1; 
    adb shell sendevent /dev/input/event6 1 116  0;
    adb shell sendevent /dev/input/event6 0 0 0
    adb shell input keyevent 20
    adb shell input keyevent 20
    adb shell input keyevent 23
    adb shell input keyevent 22
    adb shell input keyevent 23

    sleep 30

    wait_time=60
    while [ $((wait_time-=2)) -gt 0 ]
    do 
        sleep 2
        printf "."
        boot_completed=`adb -s ${device} shell getprop sys.boot_completed 2>/dev/null |sed 's/\r//'`
        if  [ ${boot_completed} -a ${boot_completed} == "1" ] ; then
            echo "boot completed "
            reboot_count=$((reboot_count+1))
            echo " reboot ${reboot_count} times, ${total} times left"
            break
        else
            continue
        fi
    done
    if [ $wait_time -eq 0 ] ; then
        echo "reboot failed, device is not up. please check the log"
        break
    fi
done
end_time=`adb -s ${device} shell date`
host_time=`date`
echo "test end at "
echo "mobile time $end_time"
echo "host time $host_time"
echo "reboot test has run ${reboot_count} times!"
