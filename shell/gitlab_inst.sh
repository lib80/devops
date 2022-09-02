#!/bin/bash

cat > /etc/yum.repos.d/gitlab-ce.repo <<- 'EOF'
[gitlab-ce]
name=Gitlab CE Repository
baseurl=https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el$releasever/
gpgcheck=0
enabled=1
EOF

yum -y install policycoreutils-python openssh-server postfix gitlab-ce