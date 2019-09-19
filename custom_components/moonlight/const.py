"""Constants for moonlight."""
# Base component constants
DOMAIN = "moonlight"
DOMAIN_DATA = "{}_data".format(DOMAIN)
VERSION = "0.0.1"
PLATFORMS = ["sensor"]
REQUIRED_FILES = [
    "const.py",
    "manifest.json",
    "sensor.py",
]
ISSUE_URL = "https://github.com/sondregronas/MOONLIGHT-HA/issues"
STARTUP = """
-------------------------------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
-------------------------------------------------------------------
"""

# Configuration
CONF_NAME              = 'name'
CONF_ICON              = 'icon'
CONF_ICON_ACTIVE       = 'icon_active'
CONF_HOST              = 'host'

# Defaults
DEFAULT_NAME           = 'Moonlight'
DEFAULT_ICON           = 'mdi:cast'
DEFAULT_ICON_ACTIVE    = 'mdi:cast-connected'