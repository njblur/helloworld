devices=`adb devices 2>/dev/null|grep -v List | awk '{print $1}'` 
devices_count=`adb devices 2>/dev/null|grep -v List | awk '{print $1}'|wc -l` 
echo $devices_count
if [ devices_count != "2" ]; then
echo "please connect 2 phones to your computer"
#exit 1
fi


echo "make sure you've done such configuration before the test"
echo "1 open the WIFI hostspot on one device."
echo "2 connect another device to this device"

echo "please any key to continue when you are ready "
#read

for device in $devices
do
ip=`adb -s $device shell netcfg |grep wlan0 |awk '{print $3 }'`
ip=${ip%/24}
if [ $ip == "192.168.1.1" ]; then
host=$device
host_ip=$ip
found_ap=1
echo " found ap"
else
client=$device
client_ip=$ip
fi
done

if [ $found_ap  -ne 1 ] ;then
echo "no host device found, did you open the hostspot?"
exit 1
fi

echo "host device"
echo "	serial number: $host"
echo "	ip : $host_ip"
echo "client device"
echo "	serial number: $client"
echo "	ip : $client_ip"
#read 

echo "pushing iperf..."

adb -s $host root
adb -s $host remount
adb -s $host push iperf2_0_4 /system/bin/
adb -s $host shell chmod 755 /system/bin/iperf2_0_4

adb -s $client root
adb -s $client remount
adb -s $client push iperf2_0_4 /system/bin/
adb -s $client shell chmod 755 /system/bin/iperf2_0_4
stop_hu.sh

echo "test starting"

echo $host $host_ip
echo $client $client_ip

adb -s $host shell iperf2_0_4 -s -u -b 50M -t 5000 -i 1 &
adb -s $client shell iperf2_0_4 -s -u -b 50M -t 5000 -i 1  & 
adb -s $client shell iperf2_0_4 -c $host_ip -u -b 50M -t 500 -i 1 & 
adb -s $host shell iperf2_0_4 -c $client_ip -u -b 50M -t 5000 -i 1 &
