#!/usr/bin/with-contenv bashio
set +e
#python3 -m http.server 8000

while :
do
CONFIG_PATH=/data/options.json

#openai_api_key="$(bashio::config 'openai_api_key')"
Refresh_rate=10000
VarCurrentTime=$(date +%H:%M:%S)
VarCurrentDate=$(date +%Y-%m-%d)



clear
#echo $openai_api_key
echo $VarCurrentDate $VarCurrentTime


python3 /main.py





echo "All Done! Waiting " $Refresh_rate " seconds to rinse and repeat."
sleep $Refresh_rate
done
