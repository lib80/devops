#!/bin/bash
# Author: libin

# 判断目标主机是否已初始化
if [ `yum grouplist installed | grep -c "Development Tools"` -gt 0 ];then
    echo 'The host had already been initialized.'
    exit 0
fi

#准备开发环境
yum -y groupinstall "Development Tools"
yum -y install epel-release vim wget mlocate lsof telnet iftop

#设置命令提示符和命令历史格式
echo 'PS1="\[\e[37;1m\][\[\e[32;1m\]\u\[\e[37;40m\]@\[\e[34;1m\]\h \[\e[0m\]\t \[\e[35;1m\]\W\[\e[37;1m\]]\[\e[m\]\\$ "' >> /etc/profile
echo 'export HISTTIMEFORMAT="%F %T `whoami` "' >> /etc/profile

#调大最大进程数
cat > /etc/security/limits.d/20-nproc.conf <<- EOF
# Default limit for number of user's processes to prevent
# accidental fork bombs.
# See rhbz #432903 for reasoning.
root       soft    nproc     unlimited
root soft nofile 65535
root hard nofile 65535
* soft nproc 65535
* hard nproc 65535
* soft nofile 65535
* hard nofile 65535
EOF

#提高ssh连接速度
sed -i -e '/GSSAPIAuthentication/c GSSAPIAuthentication no' -e '/UseDNS/c UseDNS no' /etc/ssh/sshd_config
systemctl restart sshd

#关闭selinux和firewalld
sed -i '/^SELINUX=/c SELINUX=disabled' /etc/selinux/config
systemctl stop firewalld
systemctl disable firewalld

mkdir /data
#挂载并格式化数据盘
if [ -b /dev/vdb ] && [ -z `lsblk -o FSTYPE /dev/vdb | grep -v "FSTYPE"` ]; then
    parted -s /dev/vdb mklabel gpt
    parted -s /dev/vdb mkpart primary 2048s 100%
    mkfs.ext4 /dev/vdb1
    sleep 3
    mount /dev/vdb1 /data
    echo '/dev/vdb1   /data   ext4    defaults    0  0' >> /etc/fstab
fi

#rm和systemctl命令处理
cat >> /etc/bashrc <<- EOF
alias rm='/usr/local/scripts/alias_rm.sh' cdsystem='cd /usr/lib/systemd/system/' cdnet='cd /etc/sysconfig/network-scripts/'
alias start='systemctl start' stop='systemctl stop' restart='systemctl restart' reload='systemctl reload' status='systemctl status' enable='systemctl enable' disable='systemctl disable' is-enabled='systemctl is-enabled'
EOF

#其它
mkdir /usr/local/scripts
mkdir /data/{rubbish,backupdata}
chmod 757 /data/rubbish
echo '0 2 * * * /usr/bin/rm -rf /data/rubbish/*' >> /var/spool/cron/root

chmod +x /etc/rc.d/rc.local

yum -y update kernel

#shutdown -r now
