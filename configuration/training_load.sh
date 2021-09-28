#! /bin/bash

while : ; 

    if [ $(echo "scale=2;$(date +"%M")/10" | bc ) > 5 ]; then
        sleep 0.01
    fi

    if [ $(echo "scale=2;$(date +"%M")/10" | bc ) > 4 ]; then
        sleep 0.1
    fi

    if [ $(echo "scale=2;$(date +"%M")/10" | bc ) > 3 ]; then
        sleep 60
    fi

    if [ $(echo "scale=2;$(date +"%M")/10" | bc ) > 2 ]; then
        sleep 0.01
    fi

    if [ $(echo "scale=2;$(date +"%M")/10" | bc ) > 1 ]; then
        sleep 0.1
    fi

    if [ $(echo "scale=2;$(date +"%M")/10" | bc ) > 5 ]; then
        sleep 60
    fi;

    wget -q -O- http://php-apache; 
    
done