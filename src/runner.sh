input=../input


while IFS='' read -r line || [[ -n "$line" ]]; do
    while IFS='|' read -ra ADDR; do
        python readRSS.py $2 $3 ${ADDR[0]} ${ADDR[1]} ${ADDR[2]} ${ADDR[3]} &
    done <<< $line
done < "$1"

