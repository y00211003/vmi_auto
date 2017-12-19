#!/bin/bash
# Auther :  xiang_wang@trendmicro.com.cn


cd $(readlink -e `dirname $0`)

CONF_FILE="./vmi/config.ini"
if [ ! -e $CONF_FILE ] ;then
    echo "no config file found."
    exit
fi
. ./vmi/scripts/read_ini.sh

read_ini $CONF_FILE

DROID_AUTO_CLIENT_IP=$INI__DroidAutoClient__ip
DROID_AUTO_CLIENT_USER=$INI__DroidAutoClient__user
DROID_AUTO_CLIENT_PWD=$INI__DroidAutoClient__password
TMSMW_SERVER_PORTAL_IP=$INI__UniaServer__portal_ip
TMSMW_SERVER_WEB_IP=$INI__UniaServer__web_ip

function get_latest_build_version()
{
    [ -d /mnt/autoBuildServer ] || sudo mkdir -p /mnt/autoBuildServer
    sudo umount /mnt/autoBuildServer > /dev/null 2>&1

    sudo curlftpfs ftp://10.204.16.2/Build/TMVMI/5.5/centos67/en/Rel /mnt/autoBuildServer -o user='trend\\s-dlptest:DLP_2013@test',allow_other

    declare -a build_list=$(ls /mnt/autoBuildServer)
    current_build_version=$(echo $build_list | gawk -F' ' '{print $NF}')
    if [ $current_build_version == "Latest" ];then 
        current_build_version=$(echo $build_list | gawk -F' ' '{print $(NF-1)}')
    fi
    #current_build_version=1003
    echo $current_build_version
}

function check_isofile_with_build_version()
{
    #echo "start to check"
    origin_iso_path="/mnt/autoBuildServer/$1/output/iso/TMVMI-5.5-$1-x86_64.iso"
    origin_iso_sha1file="/mnt/autoBuildServer/$1/output/iso/SHA1SUM"

    #echo "will check sha1"
    
    if [ ! -e $origin_iso_sha1file ]; then
        #echo "SHA1SUM is not ready, wait another 300 secs."
        sleep 600
        #if [ ! -e $origin_iso_path || ! -e $origin_iso_sha1file ];then
        #    return 1
        #fi
        if [ ! -e $origin_iso_path ];then
            return 1
        fi
        if [ ! -e $origin_iso_sha1file ];then
            return 1
        fi
    else
        return 0
    fi
}

function download_android_client_and_repack()
{
    #download and repack android tmsmw client
    #if [ -f "TMVMI.apk" ];then
    #    rm -f TMVMI.apk
    #fi
    #wget --no-check-certificate "https://$TMSMW_SERVER_PORTAL_IP/TMVMI.apk"

    #wget may fail
    unzip_result=1
    for i in 1 2 3
    do 
        if [ -f "TMVMI.apk" ];then
            rm -f TMVMI.apk
        fi
        wget --no-check-certificate "https://$TMSMW_SERVER_PORTAL_IP/TMVMI.apk"
        unzip -l TMVMI.apk
        unzip_result=$?
        if [ $unzip_result -eq 0 ]; then
            echo wget success
            break
        else
            echo wget fail
        fi
    done
    if [ $unzip_result -ne 0 ]; then
        echo totally fail
        
    fi

    #no need to wrap, add noSign for appium capatibility
    #./vmi/scripts/signapkwrapper/src/zrun.sh ./TMVMI.apk ./resources
    scp ./TMVMI.apk ./resources/TMVMI.sign.apk

#    scp resources/TMVMI.sign.apk root@$TMSMW_SERVER_WEB_IP:/vmi/manager/web_portal/static/TMVMI.apk
#    scp resources/TMVMI.sign.apk root@$TMSMW_SERVER_WEB_IP:/var/www/web_portal/TMVMI.apk
}

function execute_automation_with_build_version()
{

    vmi/scripts/setup_virtual_machine.sh $1

    download_android_client_and_repack

    rm -f first.xml second.xml third.xml output.xml
    rm -rf robot/temp

    echo "We are starting automation test."

    sleep 20

    #rerun 3 times
    pybot -L DEBUG -i superlab --output first.xml robot/cases/allDebug_performance.txt
    #pybot -L DEBUG -i superlab -R first.xml --output second.xml robot/cases/allDebug_performance.txt
    #pybot -L DEBUG --runmode random:test -R second.xml --output third.xml robot/cases/allDebug_performance.txt
    #pybot -L DEBUG -i client  --output first.xml robot/cases/allDebug_tags.txt
    #pybot -L DEBUG -i client  -R first.xml --output second.xml robot/cases/allDebug_tags.txt
    #pybot -L DEBUG -i client  -R second.xml --output third.xml robot/cases/allDebug_tags.txt
    if [ -f second.xml ] ;then
        if [ -f third.xml ] ;then
            rebot --outputdir ./ --output output.xml first.xml second.xml third.xml
        else
            rebot --outputdir ./ --output output.xml first.xml second.xml
        fi
    else   
        rebot --outputdir ./ --output output.xml first.xml
    fi
}

function send_notification_with_build_version()
{
    output=$(readlink -e output.xml)

    if [ -f output.xml ] ;then
        python vmi/scripts/sent_performance.py $1  $output
    fi
}


declare current_build_version
declare last_build_version=1000

if [ ! -e resources ];then
    mkdir resources
fi
umount ./resources > /dev/null 2>&1
mount -t cifs -o username="$DROID_AUTO_CLIENT_USER",password="$DROID_AUTO_CLIENT_PWD" //$DROID_AUTO_CLIENT_IP/resources  resources

if [ $# -eq 1 ];then
    current_build_version=$1
    $(check_isofile_with_build_version $current_build_version)
    if [ $? -eq 0 ]; then
        execute_automation_with_build_version $current_build_version
        send_notification_with_build_version $current_build_version
    fi
else
    while :
    do
        current_build_version=$(get_latest_build_version)
        #current_build_version=1288
        echo "current build version is "$current_build_version
        echo $last_build_version

        if [ $current_build_version -gt $last_build_version ] ;then
            echo "great"
            #sleep 300
            last_build_version=$current_build_version
            $(check_isofile_with_build_version $current_build_version)
            if [ $? -eq 0 ];then
                echo -e $current_build_version":\c" >> /root/vmi/10001001001.txt
                echo -e $current_build_version":\c" >> /root/vmi/10001001002.txt
                echo -e $current_build_version":\c" >> /root/vmi/10001001003.txt
                echo -e $current_build_version":\c" >> /root/vmi/droidLoginTime.txt
                echo -e $current_build_version":\c" >> /root/vmi/10001001004.txt
                execute_automation_with_build_version $current_build_version
                send_notification_with_build_version $current_build_version
            fi
        else
            echo "No newer build found , keep watching..."
            sleep 600
        fi

    done
fi
