from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo, format_mac
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from .const import DOMAIN
from .board import Api


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    from .board import IPX800v3

    board: IPX800v3 = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([button for button in board.get_buttons()])


class Button(ButtonEntity):
    def __init__(self, coordinator, pin: int, device: DeviceInfo, api: Api):
        super().__init__()
        self._pin = pin
        self._attr_device_info = device
        self._api = api
        self._attr_unique_id = (
            format_mac(device.get("serial_number")) + "-" + str(self._pin) + "-button"
        )
        self._attr_name = "Push button " + str(pin)
        self._coordinator = coordinator

    async def async_press(self):
        await self._api.call_api("leds.cgi?led=" + str(self._pin - 1))
        await self._coordinator.async_refresh()
