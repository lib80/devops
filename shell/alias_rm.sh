#!/bin/bash
#给rm命令创建别名，防止误操作
#author: libin

if [ "$#" -lt 1 ]; then
    echo "missing operand"
    exit 2
fi

for i in "$@"; do
    target=`basename "$i" 2> /dev/null`
    if [ $? -eq 0 ]; then
        if [ "$target" = "/" ]; then
           echo "dangerous!"
           exit 2
        fi
        if [ -e /data/rubbish/"$target" ]; then
            /usr/bin/rm -rf /data/rubbish/"$target"
        fi
        mv "$i" /data/rubbish/
    fi
done
