from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from datetime import datetime, timedelta
import pytz
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "wtime"

class WTimeDSTBinarySensor(BinarySensorEntity):
    """Representation of a WTime DST binary sensor."""

    def __init__(self, entry_id: str, timezone: str):
        """Initialize the DST sensor."""
        self._attr_name = "WTime DST Status"
        self._attr_unique_id = f"{entry_id}_dst_active"
        self._timezone = pytz.timezone(timezone)
        self._attr_is_on = self._check_dst()

    def _check_dst(self) -> bool:
        """Check if Daylight Saving Time (DST) is active."""
        try:
            now = datetime.now(self._timezone)
            dst_offset = now.dst()
            _LOGGER.debug(f"Current time: {now}, DST offset: {dst_offset}")
            return dst_offset is not None and dst_offset != timedelta(0)
        except Exception as e:
            _LOGGER.error(f"Error checking DST status: {e}")
            return False

    @property
    def is_on(self) -> bool:
        """Return True if DST is active."""
        return self._attr_is_on

    async def async_update(self):
        """Update the DST sensor state."""
        self._attr_is_on = self._check_dst()


class WTimeWeekdayBinarySensor(BinarySensorEntity):
    """Representation of a WTime Weekday binary sensor."""

    def __init__(self, entry_id: str, timezone: str):
        """Initialize the Weekday sensor."""
        self._attr_name = "WTime Is Weekday"
        self._attr_unique_id = f"{entry_id}_weekday"
        self._timezone = pytz.timezone(timezone)
        self._attr_is_on = self._check_weekday()

    def _check_weekday(self) -> bool:
        """Check if today is a weekday."""
        try:
            now = datetime.now(self._timezone)
            is_weekday = now.weekday() < 5  # Monday (0) to Friday (4)
            _LOGGER.debug(f"Current time: {now}, Is weekday: {is_weekday}")
            return is_weekday
        except Exception as e:
            _LOGGER.error(f"Error checking weekday status: {e}")
            return False

    @property
    def is_on(self) -> bool:
        """Return True if today is a weekday."""
        return self._attr_is_on

    async def async_update(self):
        """Update the Weekday sensor state."""
        self._attr_is_on = self._check_weekday()


class WTimeWeekendBinarySensor(BinarySensorEntity):
    """Representation of a WTime Weekend binary sensor."""

    def __init__(self, entry_id: str, timezone: str):
        """Initialize the Weekend sensor."""
        self._attr_name = "WTime is Weekend"
        self._attr_unique_id = f"{entry_id}_weekend"
        self._timezone = pytz.timezone(timezone)
        self._attr_is_on = self._check_weekend()

    def _check_weekend(self) -> bool:
        """Check if today is a weekend."""
        try:
            now = datetime.now(self._timezone)
            is_weekend = now.weekday() >= 5  # Saturday (5) and Sunday (6)
            _LOGGER.debug(f"Current time: {now}, Is weekend: {is_weekend}")
            return is_weekend
        except Exception as e:
            _LOGGER.error(f"Error checking weekend status: {e}")
            return False

    @property
    def is_on(self) -> bool:
        """Return True if today is a weekend."""
        return self._attr_is_on

    async def async_update(self):
        """Update the Weekend sensor state."""
        self._attr_is_on = self._check_weekend()


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the WTime binary sensors."""

    timezone = hass.config.time_zone or "UTC"
    _LOGGER.debug(f"Setting up WTimeBinarySensors with timezone: {timezone}")

    async_add_entities([
        WTimeDSTBinarySensor(entry.entry_id, timezone),
        WTimeWeekdayBinarySensor(entry.entry_id, timezone),
        WTimeWeekendBinarySensor(entry.entry_id, timezone),
    ])
