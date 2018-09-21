#! /bin/bash

if [ "$SMS_1_NUMBER" = "+79615777191" ] && [ "$SMS_1_TEXT" = "report" ]; then
    echo "Subject: Current report:" > report.txt
    echo "" >> report.txt
    echo "Current report:" >> report.txt
    echo "" >> report.txt
    echo "Temperature:" >> report.txt
    echo $(cat /sys/bus/w1/devices/28-04146da896ff/w1_slave | grep t= | sed 's|.*t=|Current temp1: |' | sed 's/./&./17') C >> report.txt
    echo $(cat /sys/bus/w1/devices/28-04146dd20dff/w1_slave | grep t= | sed 's|.*t=|Current temp2: |' | sed 's/./&./17') C >> report.txt
    echo "" >> report.txt
    echo "Shedule:" >> report.txt
    cat /opt/kotel/kotel.cfg | grep \"time >> report.txt
    echo "" >> report.txt
    echo "Kotel log:" >> report.txt
    tail -20 /var/log/sv/kotel/current | grep -v "Current" >> report.txt
    echo "" >> report.txt
    echo "System info:" >> report.txt
    echo "" >> report.txt
    echo "Uptime:" >> report.txt
    uptime >> report.txt
    echo "" >> report.txt
    echo "df:" >> report.txt
    df -h >> report.txt
    cat report.txt | msmtp -d andrdi@ya.ru > /dev/null
    rm report.txt
    exit
fi

printf "Subject: Message from $SMS_1_NUMBER: $SMS_1_TEXT

Message from $SMS_1_NUMBER
SMS Class: $SMS_1_CLASS
SMS Reference: $SMS_1_REFERENCE
SMS Message text: $SMS_1_TEXT

" | msmtp -d andrdi@ya.ru > /dev/null
