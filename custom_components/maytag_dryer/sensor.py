"""Sensor for maytag_dryer account status."""
from datetime import timedelta
import logging
import requests
import arrow
import xmltodict, json
from xml.etree import ElementTree

from time import mktime

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import track_time_interval
from homeassistant.util.dt import utc_from_timestamp

_LOGGER = logging.getLogger(__name__)

CONF_USER = "user"
CONF_PASSWORD = "password"

ICON = "mdi:tumble-dryer"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USER): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)


BASE_INTERVAL = timedelta(minutes=15)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the maytag_dryer platform."""
    
    user = config.get(CONF_USER)
    password = config.get(CONF_PASSWORD)
    entities = [maytag_dryerSensor(user,password)]
    if not entities:
        return
    add_entities(entities, True)

    # Only one sensor update once every 60 seconds to avoid
    entity_next = 0

    @callback
    def do_update(time):
        nonlocal entity_next
        entities[entity_next].async_schedule_update_ha_state(True)
        entity_next = (entity_next + 1) % len(entities)

    track_time_interval(hass, do_update, BASE_INTERVAL)


class maytag_dryerSensor(Entity):
    """A class for the mealviewer account."""

    def __init__(self, user, password):
        """Initialize the sensor."""
                
        self._name = "Dryer"
        self._user = user
        self._password = password
        
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def entity_id(self):
        """Return the entity ID."""
        
        return 'sensor.maytag_dryer_' + (self._name).lower()
        
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._status
        
    @property
    def should_poll(self):
        """Turn off polling, will do ourselves."""
        return False
        
    def update(self):
        """Update device state."""
        
        
        try:
            auth_url = "https://api.whrcloud.com/oauth/token"
            auth_header = {
                "Content-Type": "application/x-www-form-urlencoded",    
            }

            auth_data = {
                "client_id": "maytag_ios",
                "client_secret": "OfTy3A3rV4BHuhujkPThVDE9-SFgOymJyUrSbixjViATjCGviXucSKq2OxmPWm8DDj9D1IFno_mZezTYduP-Ig",
                "grant_type": "password",
                "username": self._user,
                "password": self._password,
            }

            headers = {}
            r = requests.post(auth_url, data=auth_data, headers=auth_header)
            data = r.json()

            SAID = data.get('SAID')[0]
            access_token = data.get('access_token')

            new_url = 'https://api.whrcloud.com/api/v1/appliance/' + SAID

            new_header = {
                "Authorization": "Bearer " + access_token,
                "Content-Type": "application/json",
                "Host": "api.whrcloud.com",
                "User-Agent": "okhttp/3.12.0",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
            }

            r = requests.get(new_url, data={}, headers=new_header)
            data = r.json()

            self._applianceId = data.get('applianceId')
            self._lastSynced = data.get('lastFullSyncTime')
            self._lastModified = data.get('lastModified')
            self._serialNumber = data.get('attributes').get('XCat_ApplianceInfoSetSerialNumber').get('value')
            self._doorOpen = data.get('attributes').get('Cavity_OpStatusDoorOpen').get('value')
            self._status = data.get('attributes').get('Cavity_CycleStatusMachineState').get('value')
            self._cycleName = data.get('attributes').get('Cavity_CycleSetCycleName').get('value')
            self._cycleId = data.get('attributes').get('DryCavity_CycleSetCycleSelect').get('value')
            self._manualDryTime = data.get('attributes').get('DryCavity_CycleSetManualDryTime').get('value')
            self._drynessLevel = data.get('attributes').get('DryCavity_CycleSetDryness').get('value')
            self._airflow = data.get('attributes').get('DryCavity_CycleStatusAirFlowStatus').get('value')
            self._drying = data.get('attributes').get('DryCavity_CycleStatusDrying').get('value')        
            self._damp = data.get('attributes').get('DryCavity_CycleStatusDamp').get('value')                     
            self._steaming = data.get('attributes').get('DryCavity_CycleStatusSteaming').get('value')       
            self._sensing = data.get('attributes').get('DryCavity_CycleStatusSensing').get('value') 
            self._cooldown = data.get('attributes').get('DryCavity_CycleStatusCoolDown').get('value')     
            self._temperature = data.get('attributes').get('DryCavity_CycleSetTemperature').get('value')                    
            self._operations = data.get('attributes').get('Cavity_OpSetOperations').get('value')                      
            self._powerOnHours = data.get('attributes').get('XCat_OdometerStatusTotalHours').get('value')
            self._hoursInUse = data.get('attributes').get('XCat_OdometerStatusRunningHours').get('value')    
            self._totalCycles = data.get('attributes').get('XCat_OdometerStatusCycleCount').get('value')                     
            self._remoteEnabled = data.get('attributes').get('XCat_RemoteSetRemoteControlEnable').get('value')                    
            self._timeRemaining = data.get('attributes').get('Cavity_TimeStatusEstTimeRemaining').get('value')                  
            self._online = data.get('attributes').get('Online').get('value')
                    
        except:        
            self._applianceId = None
            self._lastSynced = None
            self._lastModified = None
            self._serialNumber = None
            self._doorOpen = None
            self._status = None
            self._cycleName = None
            self._cycleId = None
            self._manualDryTime = None
            self._drynessLevel = None
            self._airflow = None
            self._drying = None
            self._damp = None        
            self._steaming = None     
            self._sensing = None
            self._cooldown = None
            self._temperature = None                  
            self._operations = None               
            self._powerOnHours = None
            self._hoursInUse = None    
            self._totalCycles = None
            self._remoteEnabled = None
            self._timeRemaining = None           
            self._online = None
    
    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attr = {}
        
        attr["applianceId"]= self._applianceId
        attr["lastSynced"]= self._lastSynced 
        attr["lastModified"]= self._lastModified 
        attr["lastModified"]= self._lastModified 
        attr["doorOpen"]= self._doorOpen 
        attr["status"]= self._status 
        attr["cycleName"]= self._cycleName 
        attr["cycleId"]= self._cycleId 
        attr["manualDryTime"]= self._manualDryTime 
        attr["drynessLevel"]= self._drynessLevel
        attr["airflow"]= self._airflow
        attr["drying"]= self._drying 
        attr["damp"]= self._damp         
        attr["steaming"]= self._steaming      
        attr["sensing"]= self._sensing 
        attr["cooldown"]= self._cooldown 
        attr["temperature"]= self._temperature                   
        attr["operations"]= self._operations                
        attr["powerOnHours"]= self._powerOnHours 
        attr["hoursInUse"]= self._hoursInUse     
        attr["totalCycles"]= self._totalCycles 
        attr["remoteEnabled"]= self._remoteEnabled 
        attr["timeRemaining"]= self._timeRemaining            
        attr["online"]= self._online 
            
        return attr

    
    @property
    def icon(self):
        """Return the icon to use in the frontend."""
        return ICON