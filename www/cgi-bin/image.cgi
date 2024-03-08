#!/bin/sh
preview=/tmp/snapshot.jpg
date=$(TZ=GMT0 date +'%a, %d %b %Y %T %Z')
echo "HTTP/1.1 200 OK
Content-type: image/jpeg
Content-Disposition: inline; filename=preview-$(date +%s).jpg
Content-Length: $(stat -c%s $preview)
Cache-Control: no-store
Pragma: no-cache
Date: $date
Expires: $date
Etag: \"$(cat /proc/sys/kernel/random/uuid)\"
Connecton: close
"
cat $preview
