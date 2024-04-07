#!/bin/sh
preview=/tmp/snapshot.jpg
echo "HTTP/1.1 200 OK
Content-Type: multipart/x-mixed-replace; boundary=frame
Pragma: no-cache
Connecton: close
"

echo -n -e "--frame\r\nContent-Type: image/jpeg\r\n\r\n"
cat $preview
echo -n -e "--frame\r\nContent-Type: image/jpeg\r\n\r\n"
while [ 1 ]
do
    cat $preview
    echo -n -e "\r\n\r\n"
    echo -n -e "--frame\r\nContent-Type: image/jpeg\r\n\r\n"
    sleep 1
done