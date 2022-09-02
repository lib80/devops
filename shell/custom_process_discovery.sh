#!/bin/bash
#author: libin

processes=(`egrep -v "^#|^$" /usr/local/zabbix/etc/zabbix_agentd.conf.d/custom_process_list.txt`)
echo -e "{\n\t\"data\": ["
if [ "${#processes[@]}" -gt 0 ]; then
    last_index=$[${#processes[@]}-1]
    for index in "${!processes[@]}"; do
        if [ "$index" -lt "${last_index}" ]; then
            echo -e "\t\t{\"{#CUSTOM}\": \"${processes[$index]}\"},"
        else
            echo -e "\t\t{\"{#CUSTOM}\": \"${processes[$index]}\"}"
        fi
    done
fi
echo -e "\t]\n}"
