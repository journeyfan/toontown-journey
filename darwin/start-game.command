cd `dirname $0`
cd ../

export TTI_GAMESERVER=127.0.0.1
read -p 'Username: ' TTI_PLAYCOOKIE
export TTI_PLAYCOOKIE=$TTI_PLAYCOOKIE

echo 'Starting Toontown...'

while true; do
    python -m toontown.toonbase.ClientStart
    read -n 1 -s -r -p "Press any key to continue..."
done