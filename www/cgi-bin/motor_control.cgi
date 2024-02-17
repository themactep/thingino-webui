#!/bin/sh

# Read the query string from environment variable
queryString=$(echo "$QUERY_STRING" | tr '&' '\n')

# Initialize variables
xStep=0
yStep=0

# Parse the query string
for param in $queryString; do
    case $param in
        x=*) xStep=${param#*=} ;;
        y=*) yStep=${param#*=} ;;
    esac
done

if ! echo "$xStep" | grep -qE '^-?[0-9]+$'; then
    echo "Content-type: text/plain"
    echo ""
    echo "Invalid x step value"
    exit
fi

if ! echo "$yStep" | grep -qE '^-?[0-9]+$'; then
    echo "Content-type: text/plain"
    echo ""
    echo "Invalid y step value"
    exit
fi

# Check if both xStep and yStep are 0, indicating a recenter command
if [ "$xStep" -eq 0 ] && [ "$yStep" -eq 0 ]; then
    # Execute the recenter command
    /bin/motors -r
    responseMsg="Motor recentered."
else
    # Execute the motors command with the validated steps
    /bin/motors -d g -x $xStep -y $yStep
    responseMsg="Motor moved: X steps $xStep, Y steps $yStep"
fi

# Return an appropriate response
echo "Content-type: text/plain"
echo ""
echo "$responseMsg"
