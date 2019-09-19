"""
The "moonlight" custom components.

moonlight:
"""
import os
from datetime import timedelta
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
import requests
from homeassistant.helpers import discovery
from homeassistant.util import Throttle

from .const import (
    DOMAIN, 
    DOMAIN_DATA,
    STARTUP,
    VERSION,
    PLATFORMS,
    REQUIRED_FILES,
    ISSUE_URL,
    CONF_HOST,
    CONF_NAME,           DEFAULT_NAME,
    CONF_ICON,           DEFAULT_ICON,
    CONF_ICON_ACTIVE,    DEFAULT_ICON_ACTIVE,
)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Optional(DOMAIN): vol.Schema(
            {
                vol.Optional(CONF_HOST):                                                 cv.string,
                vol.Optional(CONF_NAME,              default=DEFAULT_NAME):              cv.string,
                vol.Optional(CONF_ICON,              default=DEFAULT_ICON):              cv.string,
                vol.Optional(CONF_ICON_ACTIVE,       default=DEFAULT_ICON_ACTIVE):       cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

# pylint: disable=unused-argument
async def async_setup(hass, config):
    """Setup the Moonlight server platform."""
    hass.data[DOMAIN_DATA] = {}

    # Print startup message
    startup = STARTUP.format(name=DOMAIN, version=VERSION, issueurl=ISSUE_URL)
    _LOGGER.info(startup)

    # Check that all required files are present
    file_check = await check_files(hass)
    if not file_check:
        return False

    # Grab the config
    host         = config[DOMAIN].get(CONF_HOST)
    name         = config[DOMAIN].get(CONF_NAME)
    icon         = config[DOMAIN].get(CONF_ICON)
    activeicon   = config[DOMAIN].get(CONF_ICON_ACTIVE)

    # Store config in hass.data
    hass.data[DOMAIN_DATA][CONF_NAME]              = name
    hass.data[DOMAIN_DATA][CONF_ICON]              = icon
    hass.data[DOMAIN_DATA][CONF_ICON_ACTIVE]       = activeicon

    # Initiate the component
    hass.data[DOMAIN_DATA]["client"] = MoonlightSensor(hass, host)

    # Load platforms
    for platform in PLATFORMS:
        # Get platform specific configuration
        platform_config = config[DOMAIN].get(platform, {})

        hass.async_create_task(
            discovery.async_load_platform(hass, platform, DOMAIN, platform_config, config)
        )

    return True

class MoonlightSensor:
    """A class for the Moonlight Server Sensor."""

    def __init__(self, hass, host):
        self._hass   = hass
        self._host   = host

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def update_data(self):
        """Update data."""
        try:
            req  = requests.get(str('http://'+self._host+":47989/serverinfo"), timeout=1)
            data = (req.text.split('state>')[1]).split('</')[0]
            self._hass.data[DOMAIN_DATA]["data"] = data

        # Host offline or other errors
        except Exception as error:  # pylint: disable=broad-except
            self._hass.data[DOMAIN_DATA]["data"] = 'UNAVAILABLE'

async def check_files(hass):
    """Return bool that indicates if all files are present."""
    # Verify that the user downloaded all files.
    base = "{}/custom_components/{}/".format(hass.config.path(), DOMAIN)
    missing = []
    for file in REQUIRED_FILES:
        fullpath = "{}{}".format(base, file)
        if not os.path.exists(fullpath):
            missing.append(file)

    if missing:
        _LOGGER.critical("The following files are missing: %s", str(missing))
        returnvalue = False
    else:
        returnvalue = True

    return returnvalue