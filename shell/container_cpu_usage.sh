#!/bin/bash
#author: libin
#该脚本用于统计容器的cpu使用率

output_usage() {
    cat <<- EOF
Usage:
    $0 -a
        Gets the total cpu usage for all containers
    $0 -i CONTAINER_ID
        Gets the cpu usage of the specified container
EOF
    exit 2 
}

cal_cpu_usage() {
    stat_file="$1"/cpuacct.stat
    stat1=($(awk '{print $2}' "${stat_file}"))
    us1=${stat1[0]}
    sys1=${stat1[1]}
    sleep 1
    stat2=($(awk '{print $2}' "${stat_file}"))
    us2=${stat2[0]}
    sys2=${stat2[1]}
    us_delta=$((us2-us1))
    sys_delta=$((sys2-sys1))
    echo "$((us_delta+sys_delta))%"
}

# [ "$#" -eq 0 ] && output_usage

case "$1" in
  "-a")
    control_group=/sys/fs/cgroup/cpuacct/docker
    cal_cpu_usage "${control_group}"    
    ;;
  "-i")
    [ "$#" -lt 2 ] && output_usage
    control_group=$(ls -d /sys/fs/cgroup/cpuacct/docker/"$2"*)
    cal_cpu_usage "${control_group}" 
    ;;
  *)
    output_usage
    ;;
esac
