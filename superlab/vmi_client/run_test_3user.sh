#!/bin/sh

SA_IP="10.206.139.119"
domain="vmi"

userbase="10001001000"
password="mac8.6"
export LD_LIBRARY_PATH=/usr/local/gcc-4.9.2/lib

for((i=1;i<4;i++));do
let "username=$userbase+i"
echo $username
logfile=log/superlab-${username}.log
echo $logfile
> ${logfile}
echo `date` " | user ${username} starts to login VMI"
java -jar vmi_client.jar -s ${SA_IP} -u ${domain}\\${username} -p ${password} -t superlab > ${logfile} 2>&1 &
#sleep 1
done
sleep 1

