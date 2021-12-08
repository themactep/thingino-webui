#!/usr/bin/haserl
<%in _common.cgi %>
<%
tmp_file=/tmp/microbe.zip
etag_file=/var/www/.etag
if [ "development" = "$FORM_version" ]
then
  url="https://codeload.github.com/OpenIPC/microbe-web/zip/refs/heads/themactep-dev"
  zipdir="microbe-web-themactep-dev"
else
  url="https://github.com/OpenIPC/microbe-web/archive/refs/heads/main.zip"
  zipdir="microbe-web-main"
fi

gh_etag="$(curl -skIL $url | grep "ETag:" | cut -d " " -f2 | sed 's/["\r\n]//g')"

lo_etag=$(cat $etag_file)
if [ "$lo_etag" = "$gh_etag" ]; then %>
<%in _header.cgi %>
<% report_error "GitHub version matches the installed one. Nothing to update." %>
<%in _footer.cgi %>
<% else
  command="curl -skL -o /tmp/microbe.zip $url"
  output=$(curl -skL -o /tmp/microbe.zip $url 2>&1)
  result=$?
  if [ "0" -ne "$result" ]; then %>
<%in _header.cgi %>
<% report_error "$error" %>
<%in _footer.cgi %>
<% else
    redirect_to "/cgi-bin/progress.cgi"
  fi
  unzip -o -d /tmp ${tmp_file} 2>&1
  cp -av /tmp/${zipdir}/files/var/www /var/ 2>&1
  rm -rf ${tmp_file} /tmp/${zipdir} 2>&1
  echo ${gh_etag} > ${etag_file}
fi
%>