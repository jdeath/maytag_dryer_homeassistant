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
```

### Manual

1. Copy the content of `custom_components/maytag_dryer_homeassistant` into your `custom_components/Bedrock-Homeassistant folder`.
1. Restart your instance
1. Add an entry under sensors:

```yaml
- platform: maytag_dryer
    user: "name@email.com"
    password: "your password"
```
