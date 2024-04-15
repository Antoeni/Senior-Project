#!/bin/bash

echo "0" > result_output.txt
sleep 1

while true; do
    # Read the count from data_output.txt using awk
    count=$(awk -F ': ' '{print $2}' dataOutput.txt | tr -d '}')
    
    result=$(echo "scale=2; $count / 200" | bc)
    echo $result #echo result to console. remove if do not want to display in console
    echo $result > result_output.txt # put result to text file

    sleep 2
done
