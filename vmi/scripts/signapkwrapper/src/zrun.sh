#!/bin/bash
#author: xiang_wang@trendmicro.com.cn

#Usage param number assert
if [ ! $# = 2 ];then
    echo "Usage : $(basename $0) [apk_source_file] [output_path]"
    exit 1;
fi

WORK_DIR=$(dirname $0)

#check apk source file exists
SOURCE_APK_FILE_PATH=$(readlink -e $1)
echo "$SOURCE_APK_FILE_PATH"
if [ ! -f "$SOURCE_APK_FILE_PATH" ]; then
    echo "No such apk file found !"
    exit 1;
fi

OUTPUT_PATH=$(readlink -e $2)
if [ ! -d "$OUTPUT_PATH" ];then
    echo "No output path found!"
    exit 1
fi
#execute repack
cd $(dirname $(readlink -e $0))
python vmirepacker.py $SOURCE_APK_FILE_PATH $OUTPUT_PATH
cd -
