# maytag_dryer_homeassistant


This capability has now been integrated into homeassistant >2023.2.1 by mkmer. That version handles the state names differntly and has seperate entities for the durration. I am sticking with this integration, but you may like the "official" version better as it has GUI setup and no need to specifify your SAID.

Core-2021.12.1 or later required

## Installation

### HACS (prefered)

1. Add this repository to HACS as an integration: https://github.com/jdeath/maytag_dryer_homeassistant
1. Install the integration
1. Add an entry under sensors in in configuration.yaml:

```yaml
- platform: maytag_dryer
    user: "name@email.com"
    password: "your password"
    dryersaids:
      - "your dryer SAID" # done to allow multiple devices on your account. Use uppercase letters, use the "SAID" shown in the maytag app
    washersaids:
      - "your washer SAID" # done to allow multiple devices on your account. Use uppercase letters, use the "SAID" shown in the maytag app
```
Note: If you do not have a washer or a dryer, you need to have the washersaids and dryersaids keys in your configuration, just do not put a ```- "your said"``` in it. eg:
```yaml
- platform: maytag_dryer
    user: "name@email.com"
    password: "your password"
    dryersaids:
       - "your dryer SAID" # done to allow multiple devices on your account. Use uppercase letters, use the "SAID" shown in the maytag app
    washersaids:
```


### Manual

1. Copy the content of `custom_components/maytag_dryer_homeassistant` into your `custom_components/maytag_dryer_homeassistant`.
1. Restart your instance
1. Add an entry under sensors in configuration.yaml:

```yaml
- platform: maytag_dryer
    user: "name@email.com"
    password: "your password"
    dryersaids:
       - "your dryer SAID" # done to allow multiple devices on your account. Use uppercase letters, use the "SAID" shown in the maytag app
    washersaids:
       - "your washer SAID" # done to allow multiple devices on your account. Use uppercase letters, use the "SAID" shown in the maytag app
```
Note: If you do not have a washer or a dryer, you need to have the washersaids and dryersaids keys in your configuration, just do not put a ```- "your said"``` in it. eg:

```yaml
- platform: maytag_dryer
    user: "name@email.com"
    password: "your password"
    dryersaids:
       - "your dryer SAID" # done to allow multiple devices on your account. Use uppercase letters, use the "SAID" shown in the maytag app
    washersaids:
```

### Usage
You should have a sensor called sensor.maytag_dryer_"said" and/or sensor.maytag_washer_"said"(the said will be lowercase)

It is compatable with https://github.com/rianadon/timer-bar-card

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

If you want to show other attributes, you can use the entities card
```
type: entities
entities:
  - type: attribute
    entity: sensor.maytag_dryer_xxx
    attribute: applianceid
```

You can also make template sensors in your configuration.yaml
```
sensor:
  - platform: template
    sensors:
      washer_temp_setting:
        friendly_name: "Dryer Temperature"
        value_template: "{{ state_attr('sensor.maytag_dryer_xxxx', 'temperature') }}"
```
