cd "$(dirname "$0")"
cd ..
# Define some constants for our AI server:
export MAX_CHANNELS=999999
export STATESERVER=4002
export ASTRON_IP=127.0.0.1:7100
export EVENTLOGGER_IP=127.0.0.1:7198

# Get the user input:
read -p 'District name (DEFAULT: Nuttyboro): ' DISTRICT_NAME
DISTRICT_NAME=${DISTRICT_NAME:-Nuttyboro}
read -p 'Base channel (DEFAULT: 401000000): ' BASE_CHANNEL
BASE_CHANNEL=${BASE_CHANNEL:-401000000}

python \
	-m toontown.ai.ServiceStart \
	--base-channel $BASE_CHANNEL \
	--max-channels $MAX_CHANNELS \
	--stateserver $STATESERVER \
	--astron-ip $ASTRON_IP \
	--eventlogger-ip $EVENTLOGGER_IP \
	--district-name "$DISTRICT_NAME"