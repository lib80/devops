#!/bin/bash
#author:libin
#该脚本用于处理csf文件内容格式不规范的问题

if [ $# -eq 0 ];then
    echo "usage: $0 file"
    exit
fi

dos2unix -f $1
#sed -i 's/\r//g' $1
last_abnor_amount=`egrep -vc "^([AUD]|operation);" $1`

while [ ${last_abnor_amount} -gt 0 ];do
    sed -i -r '/(^operation;)|(;[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$)/!N;s/\n//g' $1
    current_abnor_amount=`egrep -vc "^([AUD]|operation);" $1`
    if [ ${current_abnor_amount} -eq ${last_abnor_amount} ];then
        exit 2
    else
        last_abnor_amount=${current_abnor_amount}
    fi
done
