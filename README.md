# maytag_dryer_homeassistant



Core-2021.12.1 or later required

## Installation

### HACS (prefered)

1. Add this repository to HACS as an integration: https://github.com/jdeath/maytag_dryer_homeassistant
1. Install the integration
1. Add an entry in configuration.yaml
1. Add an entry under sensors:

```yaml
- platform: maytag_dryer
    user: "name@email.com"
    password: "your password"
    said: "your washer SAID" # done to allow multiple devices on your account. Use uppercase letters, use the "SAID" shown in the maytag app
```

### Manual

1. Copy the content of `custom_components/maytag_dryer_homeassistant` into your `custom_components/Bedrock-Homeassistant folder`.
1. Restart your instance
1. Add an entry under sensors:

```yaml
- platform: maytag_dryer
    user: "name@email.com"
    password: "your password"
    said: "your washer SAID" # done to allow multiple devices on your account. Use uppercase letters, use the "SAID" shown in the maytag app
```

### Usage
You should have a sensor called sensor.sensor.maytag_dryer_"said"

Should be compatable with https://github.com/rianadon/timer-bar-card

```
type: custom:timer-bar-card
entity: sensor.maytag_dryer_xxxxxxx
bar_width: 35%
active_state:
  - Running
```

You can make an automation to tell you the dryer is done
```
alias: Dryer Done
description: Dryer is Done
trigger:
  - platform: state
    entity_id: sensor.maytag_dryer_xxxxx
    to:
      - Cycle Complete
      - Wrinkle Prevent
condition: []
action:
  - service: notify.mobile_app_xxxxx
    data:
      message: Dryer Done
mode: single
```
