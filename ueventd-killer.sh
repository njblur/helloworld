while true
do
    ueventd_number=`ps |grep ueventd | busybox awk '{print $2}' | busybox wc -l`
    if [ $ueventd_number -gt 3 ]; then
        for pid in `ps |grep ueventd | busybox awk '{print $2}'|busybox tail -$((ueventd_number -3))`
        do
            kill $pid
        done
    fi
sleep 60
done
