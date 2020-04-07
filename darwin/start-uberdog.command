cd `dirname $0`
cd ..
# Define some constants for our UberDOG server:
export MAX_CHANNELS=999999
export STATESERVER=4002
export ASTRON_IP=127.0.0.1:7100
export EVENTLOGGER_IP=127.0.0.1:7198

# Get the user input:
read -p 'Base channel (DEFAULT: 1000000): ' BASE_CHANNEL
BASE_CHANNEL=${BASE_CHANNEL:-1000000}

echo 'Starting UberDOG...'
while true; do
  python \
  	-m toontown.uberdog.ServiceStart \
  	--base-channel $BASE_CHANNEL \
  	--max-channels $MAX_CHANNELS \
  	--stateserver $STATESERVER \
  	--astron-ip $ASTRON_IP \
  	--eventlogger-ip $EVENTLOGGER_IP
done