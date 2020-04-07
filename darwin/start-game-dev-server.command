cd `dirname $0`
cd ../

export TTI_GAMESERVER=192.99.167.158
read -p 'Username: ' username
read -p 'Password: ' password
export TTI_PLAYCOOKIE=$username:$password

echo 'Starting Toontown...'

while true; do
    python -m toontown.toonbase.ClientStart
    read -n 1 -s -r -p "Press any key to continue..."
done