import json
import paho.mqtt.client as mqtt
import time
import requests
import os



class ConsoleColor:    
    OKBLUE = "\033[34m"
    OKCYAN = "\033[36m"
    OKGREEN = "\033[32m"        
    MAGENTA = "\033[35m"
    WARNING = "\033[33m"
    FAIL = "\033[31m"
    ENDC = "\033[0m"
    BOLD = "\033[1m" 

print(ConsoleColor.OKCYAN + "Starting GPTastic..." + ConsoleColor.ENDC, flush=True)
print("Loading configuration /data/options.json...")

# Load settings from JSON file
try:
    with open('/data/options.json') as options_file:
        json_settings = json.load(options_file)
        openai_api_key = json_settings['openai_api_key']

        ha_url = json_settings['ha_url']
        ha_port = json_settings['ha_port']
        ha_api_key = json_settings['ha_api_key']
        mqtt_broker_ip = json_settings['mqtt_broker_ip']
        mqtt_broker_port = json_settings['mqtt_broker_port']
        mqtt_user = json_settings['mqtt_user']
        mqtt_pass = json_settings['mqtt_pass']
        mqtt_topic = json_settings['mqtt_topic']


        #print(openai_api_key) #Debbug only don't expose api keys in log
        #print(ha_api_key) #Debbug only don't expose api keys in log
        print("Addon HA API Settings")
        print("HA URL:" + ha_url)
        print("HA Port:" + str(ha_port))
        print("MQTT Settings:")
        print("Broker IP:" + mqtt_broker_ip)
        print("Broker Port:" + str(mqtt_broker_port))
        print("User:" + mqtt_user)
        print("Pass:***********")
        print("Topic:" + mqtt_topic)

except Exception as e:
    logging.error(f"Failed to load settings: {e}")
    print(ConsoleColor.FAIL + "Error loading settings.json. Ensure the file exists and is valid JSON." + ConsoleColor.ENDC)
    exit()


BROKER = mqtt_broker_ip
PORT = mqtt_broker_port
TOPIC = mqtt_topic
USERNAME = mqtt_user
PASSWORD = mqtt_pass



def on_connect(client, userdata, flags, rc):
    #print(f"on_connect rc={rc}", flush=True)
    if rc == 0:
        print(ConsoleColor.OKGREEN +  "MQTT Connect success..."+ ConsoleColor.ENDC, flush=True) 
        client.subscribe(TOPIC)
    elif rc in (4, 5):
        print(ConsoleColor.FAIL +  "Login failed, check username and password..."+ ConsoleColor.ENDC, flush=True) 
    elif rc == 3:
        print(ConsoleColor.FAIL +  "MQTT Server unavailable..." + ConsoleColor.ENDC, flush=True) 

def on_message(client, userdata, msg):
    print(ConsoleColor.WARNING  + f"{msg.topic}:" + ConsoleColor.ENDC +  f"{msg.payload.decode()}" , flush=True)
    print("Posting MQTT message to OpenAI...", flush=True)
    #BOF OPEN AI *****************************************************************************************************************************
    API_KEY = openai_api_key
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}","Content-Type": "application/json"}
    data = {"model": "gpt-4o-mini","messages": [{"role": "user", "content": msg.payload.decode()}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        inCommingString = response.json()["choices"][0]["message"]["content"]
        print(response.json()["choices"][0]["message"]["content"], flush=True)
        
        #BOF HA POST DATA VIA API
        senor_name = ""
        sensor_val = ""
        #inCommingString = "testsensor,This is just a test"

        # Split only on the first comma
        parts = inCommingString.split(",", 1)

        # Must have exactly two values
        if len(parts) != 2:
            print("Invalid format: expected two comma-separated values")
        else:
            first = parts[0].strip()
            second = parts[1].strip()

            # First value may NOT contain spaces
            if not first or " " in first:
                print("Invalid format: first value contains spaces or is empty")
            # Second value may contain spaces but must not be empty
            elif not second:
                print("Invalid format: second value is empty")
            else:
                senor_name = first
                sensor_val = second
                #print("First value :", first)
                #print("Second value:", second)

        HA_URL = ha_url + ":" + str(ha_port)
        TOKEN = ha_api_key
        #"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJjZjNmYmVmM2UxNTA0NjkzYjY0YTg5YmQ2NDZkMDNmNiIsImlhdCI6MTc2OTkyNzc1MCwiZXhwIjoyMDg1Mjg3NzUwfQ.QxrYDNwg3tMgigPJCrkNfebg7rWvk_IsmAn5l_2EOkw"


        entity_id = "sensor." + senor_name
        url = f"{HA_URL}/api/states/{entity_id}"
        headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        }

        data = {
            "state": sensor_val,
            "attributes": {
                "friendly_name": senor_name,
                "icon": "mdi:text"
            }
        }


        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  
            print("Posted:" + senor_name + "->" + sensor_val, flush=True) 
            senor_name = ""
            sensor_val = ""    
            
            print(response)
        except requests.exceptions.HTTPError as e:
            print("HA Post Request failed:", e)

        #EOF HA POST DATA VIA API
    except requests.exceptions.HTTPError as e:
        print(ConsoleColor.FAIL + "Request failed:" + ConsoleColor.ENDC , e)
    #EOF OPEN AI *****************************************************************************************************************************    



client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.enable_logger()

print("Connecting...", flush=True)
client.connect(BROKER, PORT, 60)

client.loop_start()
##print(ConsoleColor.OKGREEN +  "MQTT Connected and waiting for incomming message." + ConsoleColor.ENDC, flush=True)


while True:
    time.sleep(1)
