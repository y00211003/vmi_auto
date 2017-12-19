#!/bin/bash

echo "SSH remote access with out prompt password"

if [[ !  $# == 3 ]]; then
    echo "Hit $0 [ host ip ] [ user name ] [ password ]"
    exit 1
fi

if [ -f ~/.ssh/id_rsa.pub ]; then
    echo "Exist id_rsa.pub"
else
    echo "Not exist id_rsa.pub"
fi

if [ -f ~/.ssh/known_hosts ] ; then
    rm ~/.ssh/known_hosts
fi

remote_host=$1
remote_user=$2
remote_password=$3

if [ ! -e /usr/bin/sshpass ] ; then
    echo "Not exist sshpass"
    exit 1
fi

if [ ! -e /usr/bin/expect ] ; then
    echo "Not exist expect"
fi
setup_pub_key(){
    #remote_user=$1
    #remote_host=$2
    #remote_password=$3

expect - <<EOF
spawn ssh -oStrictHostKeyChecking=no -oCheckHostIP=no  $1@$2
expect "password"
send "$3\r"
expect "#"
send "exit\r"
EOF

    sshpass -p $remote_password ssh $remote_user@$remote_host " [ -d ~/.ssh ] || mkdir -p ~/.ssh"
    cat ~/.ssh/id_rsa.pub | sshpass -p $remote_password ssh $remote_user@$remote_host 'cat > ~/.ssh/authorized_keys'
    sshpass -p $remote_password ssh $remote_user@$remote_host "chmod 700 ~/.ssh; chmod 640 ~/.ssh/authorized_keys"
}


setup_pub_key $remote_user $remote_host $remote_password
execute_prefix="sshpass -p $remote_password ssh $remote_user@$remote_host "

sshpass -p $remote_password ssh $remote_user@$remote_host " [ -d ~/.ssh ] || mkdir -p ~/.ssh"
cat ~/.ssh/id_rsa.pub | sshpass -p $remote_password ssh $remote_user@$remote_host 'cat > ~/.ssh/authorized_keys'
sshpass -p $remote_password ssh $remote_user@$remote_host "chmod 700 ~/.ssh; chmod 640 ~/.ssh/authorized_keys"


#disable selinux

cmd="selinuxenabled && echo enabled || echo disabled"
output=$($execute_prefix $cmd)

if [ "$output" = "disabled" ];then
   echo "selinux disabled."
else
   echo "dsiableing selinux..."
   $execute_prefix /vmi/manager/manage.py disable_selinux
   $execute_prefix setenforce 0
fi


cmd="sed -i '/^bind/c\bind 0.0.0.0' /etc/redis.conf"
echo $cmd
$execute_prefix $cmd
$execute_prefix service vmiengine stop

$execute_prefix 'sed -i "s/^:INPUT DROP/:INPUT  ACCEPT/g" /vmi/manager/etc/iptables-ip'
$execute_prefix 'sed -i "s/^:INPUT  DROP/:INPUT  ACCEPT/g" /vmi/manager/etc/iptables-nat-ip'
#$execute_prefix sed -i "s/\${dbsettings\[0\]}\.\*/\*\.\*/" /vmi/manager/default.sh
$execute_prefix sed -i "s/localhost/\'\%\'/" /vmi/manager/default.sh
$execute_prefix service httpd stop
$execute_prefix service vmiengine stop
$execute_prefix service redis stop
$execute_prefix /usr/bin/mysql <<EOF
drop database vmi;
EOF
$execute_prefix /vmi/manager/default.sh
$execute_prefix service redis start
$execute_prefix service vmiengine start
$execute_prefix service httpd start
scp -r tcproxy-0.0.1-1.x86_64.rpm root@$remote_host:/root/
$execute_prefix rpm -ivUh /root/tcproxy-0.0.1-1.x86_64.rpm
