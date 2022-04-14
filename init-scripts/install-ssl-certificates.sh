#!/bin/bash
#
# File: install-ssl-certificates.sh
# Author: Alex Ott
# Created: Tuesday, September 28 2021
#

#set -x

# Update this list of certificates
declare -a certs=("/dbfs/tmp/myCA.pem" "/dbfs/tmp/myCA2.pem")

mkdir -p /usr/share/ca-certificates/extra
CERTIFI_HOME="$(python -m certifi 2>/dev/null)"
J_HOME="$(dirname $(realpath $(which java)))/.."

for cert in ${certs[@]}; do
    BNAME="$(basename $cert)"
    echo "cert=$cert BNAME=$BNAME"
    cp $cert  /usr/share/ca-certificates/extra/$BNAME
    echo "extra/$BNAME" >> /etc/ca-certificates.conf
    if [ -n "$CERTIFI_HOME" ]; then
        cat $cert >> $CERTIFI_HOME
    fi
    keytool -importcert -keystore ${J_HOME}/lib/security/cacerts -file $cert -alias $(basename $cert .pem) -storepass changeit -noprompt
done

update-ca-certificates

#keytool -list -keystore ${J_HOME}/lib/security/cacerts -storepass changeit
