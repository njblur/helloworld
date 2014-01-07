#! /bin/bash

for i in `seq 1 120`
do
	echo this test lasts $(($i*10)) minutes
	./start_iperf.sh
	sleep 10m
	./stop_iperf.sh
done
