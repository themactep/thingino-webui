#!/bin/sh

# set parameters from cli, if empty
[ -z "$mode" ] && mode=$1
[ -z "$type" ] && type=$2

case "$type" in
	ir850 | ir940 | whled)
		pin=$(fw_printenv -n gpio_${type})
		;;
	*)
		# select first non-empty pin of available
		for type in ir850 ir940 whled; do
			pin=$(fw_printenv -n gpio_${type})
			[ -n "$pin" ] && break
		done
		# set most common type for error message below
		type=ir850
		;;
esac

if [ -z "$pin" ]; then
	echo "Please define LED GPIO pin"
	echo "fw_setenv gpio_${type} <pin>"
	exit 1
fi

case "$mode" in
	on | 1)
		gpio set $pin >/dev/null
		;;
	off | 0)
		gpio clear $pin >/dev/null
		;;
	~ | toggle)
		gpio toggle $pin >/dev/null
		;;
	*)
		echo "Unknown mode"
		exit 3
		;;
esac

exit 0
