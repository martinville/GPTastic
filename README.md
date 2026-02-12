# GPTastic Home Assistant Add-on

## Overview

GPTastic is a Home Assistant add-on that acts as a bridge between MQTT, OpenAI, and Home Assistant entities.
It listens for incoming MQTT messages, forwards those messages to the OpenAI API for processing, validates
the response, and then updates a Home Assistant entity based on the result.

The add-on is designed to integrate AI-driven decisions into Home Assistant automations in a structured
and predictable way.

## ☕ Support This Project

If you find this project useful, consider supporting it:

[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-yellow?style=for-the-badge&logo=buy-me-a-coffee)](https://www.buymeacoffee.com/YOUR_USERNAME)

Or visit: [https://www.buymeacoffee.com/YOUR_USERNAME](https://buymeacoffee.com/mailmartins)


---

## What the Add-on Does

At a high level, GPTastic:

- Subscribes to an MQTT topic
- Receives messages from Home Assistant or external systems
- Sends those messages to the OpenAI API
- Requires the AI to respond in a strict CSV format:
  ```
  entity_name,value
  ```
- Validates the response format
- Updates the specified Home Assistant entity with the provided value

This allows AI-generated decisions or text to be safely consumed by Home Assistant automations.

---

## Workflow Steps

### 1. GPTastic Add-on Startup
- The GPTastic add-on starts.
- It subscribes to the MQTT topic:
  ```
  gptastic/incoming
  ```

### 2. MQTT Message Published
- An MQTT client publishes a message to the Home Assistant MQTT broker.
- The message is sent on:
  ```
  gptastic/incoming
  ```

Example payload:
```
Use my inverter battery tonight and check if tomorrow will have enough solar to recharge it.
```

### 3. GPTastic Sends Request to OpenAI
- GPTastic receives the MQTT message.
- It sends the message to the OpenAI API.
- GPTastic instructs the AI to respond only in the following CSV format:
  ```
  entity_name,value
  ```

Example response:
```
gptastic_usebattery,No
```

### 4. CSV Validation
- GPTastic receives the AI response.
- It verifies that:
  - The response is valid CSV
  - Exactly two values are present
  - The first value is an entity name
  - The second value is the entity state or value

Invalid responses are rejected.

### 5. Update Home Assistant Entity
- GPTastic uses the validated CSV data.
- It updates the Home Assistant entity specified in the response.
- The entity state is set to the provided value.

Example result:
```
sensor.gptastic_usebattery = No
```

---

## Example Use Cases

### Battery Usage Decision
**MQTT Input**
```
Should I use the inverter battery tonight based on tomorrow’s solar forecast?
```

**AI Response**
```
gptastic_usebattery,Yes
```

**Home Assistant Result**
- `sensor.gptastic_usebattery` is set to `Yes`
- Automations can act on this value

### Mode Selection
**MQTT Input**
```
Decide which operating mode the system should use tomorrow.
```

**AI Response**
```
gptastic_mode,eco
```

**Home Assistant Result**
- `sensor.gptastic_mode` is set to `eco`

---

## Summary

GPTastic enables controlled use of AI-generated decisions inside Home Assistant by:

- Receiving prompts over MQTT
- Delegating reasoning to OpenAI
- Enforcing strict response formatting
- Updating Home Assistant entities safely

This makes it suitable for automation scenarios where AI output must remain predictable and structured.
