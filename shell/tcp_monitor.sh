#!/bin/bash
# 该脚本用于监控统计tcp连接状态
# author: libin

tcp_info=$(ss -tan | sed '1d')
tcp_total=$(echo "${tcp_info}" | wc -l)
tcp_conn_info=$(echo "${tcp_info}" | grep -Ev "^LISTEN")
if [ "${tcp_total}" -gt 1000 ]; then
    file_name=$(pwd)/tcp_status_$(date +%Y-%m-%d-%H:%M).log
    echo -e "$(echo \"${tcp_info}\" | awk '{state[$1]++}END{for (s in state) {print s,state[s]}}')\nTOTAL \"${tcp_total}\"\n" >> "${file_name}"
    echo -e "对端ip及其连接数\n$(echo \"${tcp_conn_info}\" | awk '{lens=split($5,client,":");ip[client[lens-1]]++}END{for (i in ip) print i,ip[i]}' | sort -rn -k 2)\n" >> "${file_name}"
    for ip in $(echo "${tcp_conn_info}" | awk -F '[ :]+' '{print $(NF-2)}' | sort | uniq); do
        echo -e "$ip:\n$(echo \"${tcp_conn_info}\" | grep $ip | awk '{state[$1]++}END{for (s in state) {print s,state[s]}}')\n" >> "${file_name}"
    done
fi
