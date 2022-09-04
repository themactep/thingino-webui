#!/bin/sh

SUPPORTED="goke hisilicon"
[ -z "$(echo $SUPPORTED | sed -n "/\b$(ipcinfo --vendor)\b/p")" ] &&
  echo "Playing on speaker is not supported on your camera!" && exit 1

plugin="speaker"
config_file="/etc/webui/${plugin}.conf"
curl_timeout=100

log_file=/tmp/webui/${plugin}.log
mkdir -p $(dirname $log_file)
:>$log_file

show_help() {
  echo "Usage: $0 [-u url] [-f file] [-v] [-h]
  -u url      Audio URL.
  -f file     Audio file.
  -v          Verbose output.
  -h          Show this help.
"
  exit 0
}
# read variables from config
[ -f "$config_file" ] && source $config_file

# override config values with command line arguments
while getopts f:u:vh flag; do
  case ${flag} in
  f) speaker_file=${OPTARG} ;;
  u) speaker_url=${OPTARG} ;;
  v) verbose=1 ;;
  h) show_help ;;
  esac
done

[ "false" = "$speaker_enabled" ] &&
  echo "Playing on speaker is disabled in config ${config_file}." && exit 10

[ "false" = "$(yaml-cli -g .audio.enabled)" ] &&
  echo "Playing on speaker is disabled in Majestic." && exit 11

# validate mandatory values
[ -z "$speaker_url" ] &&
  echo "Speaker URL is not set" && exit 12
[ -z "$speaker_file" ] &&
  echo "Audio file is not set" && exit 13
[ ! -f "$speaker_file" ] &&
  echo "Audio file ${speaker_file} not found" && exit 14

command="curl"
[ "1" = "$verbose" ] && command="${command} --verbose"
command="${command} --connect-timeout ${curl_timeout}"
command="${command} --max-time ${curl_timeout} -X POST"

# SOCK5 proxy, if needed
if [ "true" = "$webhook_socks5_enabled" ]; then
  source /etc/webui/socks5.conf
  command="${command} --socks5-hostname ${socks5_host}:${socks5_port}"
  command="${command} --proxy-user ${socks5_login}:${socks5_password}"
fi

command="${command} -T ${speaker_file}"
command="${command} --url ${speaker_url}"

echo "$command" >>$log_file
eval "$command" >>$log_file 2>&1

[ "1" = "$verbose" ] && cat $log_file

exit 0
