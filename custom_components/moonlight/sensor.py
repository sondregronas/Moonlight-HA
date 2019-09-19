"""Sensor platform for Moonlight."""
from homeassistant.helpers.entity import Entity
from .const import (
DOMAIN,
DOMAIN_DATA, 

CONF_NAME, 
CONF_HOST,
CONF_ICON,
CONF_ICON_ACTIVE,
)

async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):  # pylint: disable=unused-argument
    """Setup sensor platform."""

    name = hass.data[DOMAIN_DATA][CONF_NAME]
    icon = hass.data[DOMAIN_DATA][CONF_ICON]
    activeicon = hass.data[DOMAIN_DATA][CONF_ICON_ACTIVE]

    async_add_entities([MoonlightSensor(hass, discovery_info, name, icon, activeicon)], True)

class MoonlightSensor(Entity):
    """Moonlight Sensor class."""
    def __init__(self, hass, config, name, icon, activeicon):
        self._hass       = hass
        self._state      = 'Unavailable'
        self._name       = name
        self._icon       = icon
        self._deficon    = icon
        self._activeicon = activeicon

    async def async_update(self):
        """Update the sensor."""

        # Issue update command
        await self._hass.data[DOMAIN_DATA]["client"].update_data()

        # Get stream status
        try:
            data = self._hass.data[DOMAIN_DATA]["data"]

            if 'UNAVAILABLE' in data:
                self._state = 'Unavailable'
                self._icon  = self._deficon
                return

            if 'BUSY' in data:
                self._state = 'Streaming'
                self._icon  = self._activeicon
                return

            if 'AVAILABLE' in data:
                self._state = 'Not streaming'
                self._icon  = self._deficon
                return

        except:
            # Host PC is Offline or Unavailable
            self._state = 'Unavailable'
            self._icon  = self._deficon
            return

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon