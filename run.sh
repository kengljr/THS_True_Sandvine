#!/bin/bash
IFS="
"
list_ip="10.185.209.8
10.185.209.11
10.185.209.14
10.185.209.17
10.185.209.20
10.185.209.23"

list_ip="${1}"
ip_check=""

networksetup -connectpppoeservice "True VPN"
vpn_status=`networksetup -showpppoestatus "True VPN"`
while [ "${vpn_status}" != "connected" ]
do
  networksetup -connectpppoeservice "True VPN"
  vpn_status=`networksetup -showpppoestatus "True VPN"`
  echo ${vpn_status}
  sleep 0.5
done

route delete -net 10.0.0.0/8 -gateway 192.168.42.1
route add -net 10.0.0.0/8 -gateway 192.168.42.1

chr()
{
  IFS=" "
  unset ip_add
  for ascii in `echo $1 | sed 's/\./ /g'`
  do
    character=$(printf \\$(printf '%03o' ${ascii}))
    ip_add=`echo ${ip_add}${character}`
  done ;
  echo ${ip_add}
}
for check_ip in ${list_ip}
  do
  printf "\n${check_ip}\n\n"
  for raw_string in `snmpwalk -v 2c -c eUr0pa ${check_ip} 1.3.6.1.4.1.15397.3.3.2.15.19 | awk 'NR>2'`
      do
        ip=`echo ${raw_string} | cut -c 112-152`
        status=`echo ${raw_string} | awk -F ' ' '{print $NF}'`
        real_ip=`chr ${ip} | sed -e 's/\///g' -e 's/://g'`
        #echo "${real_ip} : ${status}"
        if [[ ${real_ip} != "10."* ]]
        then
          real_ip=`echo "1${real_ip}"`
        fi
          
        
        if [ ${status} -ne 5 ]
          then
          ip_check+="${real_ip} "  
          #echo "${ip_check}"
        fi
      done ;
  echo "${ip_check}" | sed 's/.$//'
  python3 check.py ${check_ip} ${ip_check}
  unset ip_check
  done ;