#!/bin/bash
# Auther : xiang_wang
# Email: xiang_wang@trendmicro.com.cn

ESXHOST="10.206.137.22"
ESXPASSWD="trend#1.."
VMIVM="richard-auto-debug-vmiServer-192.168.20.201"
VMIIP="192.168.20.201"

if [ -f ~/.ssh/id_rsa.pub ]; then
    echo "Exist id_rsa.pub"
else
    echo "Not exist id_rsa.pub"
fi

if [ -f ~/.ssh/known_hosts ] ; then
    rm ~/.ssh/known_hosts
fi

function setup_pub_key(){
    remote_user=$1
    remote_host=$2
    remote_password=$3

expect - <<EOF
spawn ssh -oStrictHostKeyChecking=no -oCheckHostIP=no  $remote_user@$remote_host
expect "password"
send "$remote_password\r"
expect "#"
send "exit\r"
EOF

    sshpass -p $remote_password ssh $remote_user@$remote_host " [ -d ~/.ssh ] || mkdir -p ~/.ssh"
    cat ~/.ssh/id_rsa.pub | sshpass -p $remote_password ssh $remote_user@$remote_host 'cat > ~/.ssh/authorized_keys'
    sshpass -p $remote_password ssh $remote_user@$remote_host "chmod 700 ~/.ssh; chmod 640 ~/.ssh/authorized_keys"
}

function ssh_upload_file()
{
    remote_user=$1
    remote_host=$2
    remote_password=$3
    source_path=$4
    dist_path=$5
    echo "start to deploy scripts.."

    expect - <<EOF
spawn scp -r $source_path $remote_user@$remote_host:$dist_path
expect "password"
send "$remote_password\r"
expect "#"
EOF
}


function sshfs_mount()
{
    remote_user=$1
    remote_host=$2
    remote_password=$3
    remote_path=$4
    local_path=$5
    echo $remote_password | sshfs $remote_user@$remote_host:$remote_path $local_path -o workaround=rename -o password_stdin
}


function check_port_open()
{
    nc -w 10 -z $1 $2 > /dev/null 2>&1
    echo $?
}

function check_port_open_within_time ()
{
    count=0
    while [ $count -lt `expr $3 / 10` ]; do
        echo "checking $1 with port $2 ..."
        result=$(check_port_open $1 $2)
        if [ $result  -eq 0 ];then
            break
        else
            echo "server is not ready yet !"
            sleep 10
        fi
    done
    return $result
}

CPATH=$PWD\/$(dirname $0)
cd $CPATH

[ -d originalISO ]  || mkdir originalISO
sudo umount originalISO > /dev/null 2>&1

if [ ! -d tmp ]; then
    mkdir tmp
else
    echo clean tmp folder
    sudo rm -rf ./tmp
    mkdir tmp
fi

[ -d /mnt/autoBuildServer ] || sudo mkdir -p /mnt/autoBuildServer
sudo umount /mnt/autoBuildServer > /dev/null 2>&1

[ -d esxi ] || mkdir esxi
sudo umount esxi > /dev/null 2>&1

sudo rm -f *.iso

#sudo curlftpfs ftp://10.204.16.2/Build/TMVMI/5.3/centos67/jv/Rel /mnt/autoBuildServer -o user='trend\\s-dlptest:DLP_2013@test',allow_other
sudo curlftpfs ftp://10.204.16.2/Build/TMVMI/5.5/centos67/en/Rel /mnt/autoBuildServer -o user='trend\\s-dlptest:DLP_2013@test',allow_other

declare -a build_list=$(ls /mnt/autoBuildServer)
#current_build_version=$(echo $build_list | gawk -F' ' '{print $(NF-2)}')
current_build_version=$1
#current_build_version=1311
echo current build version is $current_build_version

#origin_iso_path=/mnt/autoBuildServer/$current_build_version/output/iso/ASVM-5.3-$current_build_version-x86_64.iso
origin_iso_path=/mnt/autoBuildServer/$current_build_version/output/iso/TMVMI-5.5-$current_build_version-x86_64.iso

if [ ! -e $origin_iso_path ]; then
    echo "No available build find for VMI"
    exit 1
fi

origin_iso=$(basename $origin_iso_path)
echo $origin_iso

echo copy iso file from CI build path ...
pv $origin_iso_path > $origin_iso
sudo mount -o loop $origin_iso originalISO

cp -rf originalISO/* ./tmp
cp -f originalISO/.discinfo ./tmp
#sed -i "/^network/c network --bootproto=static --device=eth0 --onboot=on --ip=192.168.10.201 --netmask=255.255.255.0  --nameserver=10.64.1.55 --gateway=192.168.10.1\r\nnetwork --bootproto=static --device=eth1 --onboot=on --ip=192.168.10.202 --netmask=255.255.255.0  --nameserver=10.64.1.55 --gateway=192.168.10.1" ./tmp/ks.cfg
sed -i "/^network/c network --bootproto=static --device=eth0 --onboot=on --ip=192.168.20.201 --netmask=255.255.255.0 --nameserver=10.64.1.55 --gateway=192.168.20.1" ./tmp/ks.cfg
#sed -i "/^network --bootproto/a network --bootproto=static --device=eth1 --onboot=on --ip=192.168.10.202 --netmask=255.255.255.0 --nameserver=10.64.1.55 --gateway=192.168.10.1" ./tmp/ks.cfg

sed -i "s/biosdevname=0/biosdevname=0 quiet silence/" ./tmp/isolinux/isolinux.cfg
sed -i "/prompt 1/a timeout 1" ./tmp/isolinux/isolinux.cfg
#for root ssh
sed -i "/^EOF/a sed -i \"/^PermitRootLogin without-password/c PermitRootLogin yes\" /etc/ssh/sshd_config \nservice sshd restart" ./tmp/ks.cfg

silence_iso=TMSMW-Silent-$current_build_version-x86_64.iso
echo $silence_iso
sudo mkisofs -J -r -T -R -V -v -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o TMSMW-Silent-$current_build_version-x86_64.iso ./tmp
#sudo mkisofs -J -T -R -V -v -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -o TMSMW-Silent-$current_build_version-x86_64.iso ./tmp


setup_pub_key "root" $ESXHOST $ESXPASSWD
sshfs_mount "root" $ESXHOST $ESXPASSWD /vmfs/volumes/VM_datastore/SilentISO esxi
./rebase_vm_to_snapshot.py -s $ESXHOST -u root -p $ESXPASSWD -o init -t $VMIVM
#ssh_upload_file root 10.64.88.14 trend#11 $silence_iso /vmfs/volumes/datastore1/VMIISO
cp -f $silence_iso esxi
./select_cdrom_device.py -s $ESXHOST -u root -p $ESXPASSWD -d iso  -t $VMIVM -i "[VM_datastore] SilentISO/$silence_iso"
./power_trigger.py -s $ESXHOST -u root -p $ESXPASSWD -t $VMIVM -g on

check_port_open_within_time $VMIIP 443 900

if [ $? -eq 0 ];then
    echo "Server is ready! Let us wait for a min before starting automation testting"
    sleep 30
    echo "Prepare testing environment..."
    ./prepare.sh $VMIIP root trend#1
else
    echo "Server started failed!"
fi
