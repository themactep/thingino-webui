#!/usr/bin/haserl --upload-limit=2048 --upload-dir=/tmp
<%
maxsize=2097152
magicnum="27051956"

sysupgrade_date=$(ls -lc --full-time /usr/sbin/sysupgrade | xargs | cut -d " " -f 6)
sysupgrade_date=$(date --date="$sysupgrade_date" +"%s")
new_sysupgrade_date=$(date --date="2021-12-07" +"%s")

error=""
if [ -z "$FORM_upfile_name"  ]; then
  error="no file found! Did you forget to upload?"
elif [ ! -r "$FORM_upfile" ]; then
  error="cannot read file \"${FORM_upfile_name}\" from \"${FORM_upfile}\"!"
elif [ "$(wc -c "$FORM_upfile" | awk '{print $1}')" -gt "$maxsize" ]; then
  error="file \"${FORM_upfile_name}\" is too large! Its size is $(wc -c "$FORM_upfile" | awk '{print $1}') bytes, but it should be ${maxsize} bytes or less."
elif [ "$magicnum" -ne "$(xxd -p -l 4 "$FORM_upfile")" ]; then
  error="File magic number does not match. Did you upload a wrong file? $(xxd -p -l 4 "$FORM_upfile") != $magicnum"
elif [ "$sysupgrade_date" -ge "$new_sysupgrade_date" ]; then
  error="This feature requires the latest sysupgrade tool. Please upgrade firmware first."
fi

if [ ! -z "$error" ]; then %>
<%in _header.cgi %>
<% report_error "$error" %>
<%in _footer.cgi %>
<% else
  redirect_to "/cgi-bin/progress.cgi"

  mv ${FORM_upfile} /tmp/${FORM_upfile_name}
  sysupgrade --kernel=/tmp/${FORM_upfile_name}
fi
%>