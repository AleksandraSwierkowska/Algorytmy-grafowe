#!/bin/bash

function appendAgregates() {
        isMean=$1
        isMin=$2
        isMax=$3
        file=$4

        ext=".mod"
        cp $file $file$ext
        column_nmb=$(cat $file | head -n1 | tr "," " " | wc -w)
        if [ "$isMean" != "0" ] ; then
                for ((col=1;col<=column_nmb;col++)); do
                        column=$(cat $file | tail -n +2 | tr -d " "| cut -d"," -f $col)
                        rows=$(echo $column | | wc -w)
                        sum=$(echo $column | paste -sd+ | bc)
                        mean=$(echo "scale=2 ; $sum / $rows" | bc)
                        if [ $col -eq $column_nmb ] ; then
                                echo "$mean">>$file$ext
                        else
                                echo -n "$mean,">>$file$ext
                        fi
                done
        fi

        if [ "$isMin" != "0" ] ; then
                for ((col=1;col<=column_nmb;col++)); do
                        column=$(cat $file | tail -n +2 | tr -d " "| cut -d"," -f $col)
                        min=$(echo $column | sort -n | head -n1)
                        if [ $col -eq $column_nmb ] ; then
                                echo "$min">>$file$ext
                        else
                                echo -n "$min,">>$file$ext
                        fi
                done
        fi

        if [ "$isMax" != "0" ] ; then
                for ((col=1;col<=column_nmb;col++)); do
                        column=$(cat $file | tail -n +2 | tr -d " "| cut -d"," -f $col)
                        max=$(echo $column | sort -nr | head -n1)
                        if [ $col -eq $column_nmb ] ; then
                                echo "$max">>$file$ext
                        else
                                echo -n "$max,">>$file$ext
                        fi
                done
        fi
}

isMax=1
isMin=1
isMean=1
filesNumber=0

while [ "$1" != "" ] ; do
        case $1 in
                --noMax )
                isMax=0
                ;;
                --noMin )
                isMin=0
                ;;
                --noMean )
                isMean=0
                ;;
                -h | --help)
                filesNumber=$(($filesNumber+1))
                echo -e "podsumowanie - calculates minimum, maximum and mean of every column of the CSV file (excluding the header)
and creates new file with 'mod' extension, which adds all of them at the end of each column.

                --noMax        doesn't add maximum to the CSV file
                --noMin        doesn't add minimum to the CSV file
                --noMean       doesn't add mean to the CSV file
                -h | --help    displays this help panel"
                ;;
                * )
                filesNumber=$(($filesNumber+1))
                appendAgregates "$isMean" "$isMin" "$isMax" "$1"
        esac
        shift
done

if [ "$filesNumber" == "0" ] ; then
        fromFile=$(</dev/stdin)
        fromFile= $(echo $fromFile > "file")
        appendAgregates "$isMean" "$isMin" "$isMax" "file"
        rm "file"
fi
