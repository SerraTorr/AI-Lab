#!/bin/bash

for j in 1 2 3 4 5 6 7 8 9
do
    for i in 1 2 3 4 5 6 7 8 9 10 11 12 13
    do
        for k in 0 1 2
        do
            echo -n $k $i $j
            python3 maze_retrival.py $i $j $k > test1.txt && python3 180010033.py test1.txt
        done
    done
done
