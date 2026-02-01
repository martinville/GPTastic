# GPTastic Add-on Documentation

## Purpose

This document explains how to configure and use the GPTastic Home Assistant add-on.
It focuses on **initial setup**, **configuration fields**, and **how data flows through the system**.

GPTastic relies on MQTT for input, OpenAI for processing, and the Home Assistant API for updating entities.

---

## Prerequisites

Before setting up GPTastic, ensure you have:

- Home Assistant OS or Supervised installation
- An MQTT broker configured in Home Assistant
- A Long-Lived Access Token from Home Assistant
- An OpenAI API key
- Network access between the add-on, MQTT broker, and Home Assistant

---

## Configuration Overview

GPTastic is configured through the add-on configuration UI.
Each field must be completed correctly for the add-on to function.

All configuration values are required unless stated otherwise.

---

## Configuration Fields

### OpenAI API Key

**Field:** `openai_api_key`  
**Description:**  
Your OpenAI API key used to authenticate requests to the OpenAI API.

**How to obtain:**
1. Log in to your OpenAI account
2. Create a new API key
3. Copy and paste it into this field

---

### Home Assistant API Key

**Field:** `ha_api_key`  
**Description:**  
A long-lived access token used to authenticate with the Home Assistant REST API.

**How to obtain:**
1. Open Home Assistant
2. Go to **Profile**
3. Create a **Long-Lived Access Token**
4. Copy and paste the token into this field

---

### Home Assistant URL

**Field:** `ha_url`  
**Description:**  
The base URL of your Home Assistant instance.

**Examples:**
```
http://homeassistant.local
http://192.168.1.10
```

Do not include the port in this field.

---

### Home Assistant Port

**Field:** `ha_port`  
**Description:**  
The port number Home Assistant is running on.

**Default:**
```
8123
```

---

### MQTT Broker IP

**Field:** `mqtt_broker_ip`  
**Description:**  
The hostname or IP address of the MQTT broker.

**Examples:**
```
core-mosquitto
localhost
192.168.1.20
```

---

### MQTT Broker Port

**Field:** `mqtt_broker_port`  
**Description:**  
The port used by the MQTT broker.

**Default:**
```
1883
```

---

### MQTT Username

**Field:** `mqtt_user`  
**Description:**  
The username used to authenticate with the MQTT broker.

Leave empty only if your broker allows anonymous access.

---

### MQTT Password

**Field:** `mqtt_pass`  
**Description:**  
The password used to authenticate with the MQTT broker.

---

### MQTT Topic

**Field:** `mqtt_topic`  
**Description:**  
The MQTT topic that GPTastic subscribes to for incoming prompts.

**Default:**
```
gptastic/incoming
```

---

## How GPTastic Uses These Settings

1. Connects to the MQTT broker using the provided credentials
2. Subscribes to the configured MQTT topic
3. Sends incoming messages to the OpenAI API
4. Validates the AI response format
5. Updates Home Assistant entities via the REST API

---

## Example Message Flow

**MQTT Payload:**
```
Should I use the inverter battery tonight based on tomorrow’s solar forecast?
```

**Expected AI Response:**
```
gptastic_usebattery,No
```

**Home Assistant Result:**
```
sensor.gptastic_usebattery = No
```

Automations can then react to this entity state.

---

## Troubleshooting

### No entity updates
- Verify Home Assistant URL and port
- Confirm API token permissions
- Check Home Assistant logs

### No MQTT messages received
- Verify broker IP and port
- Confirm topic name matches exactly
- Check MQTT authentication

### Invalid AI responses
- Ensure prompts instruct the AI to return CSV only
- Responses must contain exactly two values

---

## Notes

- GPTastic enforces strict CSV output
- Invalid or malformed responses are ignored
- The add-on does not create automations automatically
- Restart the add-on after changing configuration values

---

## Summary

This document describes how to configure GPTastic and explains how each configuration field is used.
Correct configuration is essential for reliable operation.
