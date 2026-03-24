import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from . import CONF_ALPICOOL_ID, AlpicoolDevice, alpicool_ns

CONF_TARGET_TEMPERATURE = "target_temperature"
CONF_RIGHT_TARGET_TEMPERATURE = "right_target_temperature"

AlpicoolTemperatureNumber = alpicool_ns.class_(
    "AlpicoolTemperatureNumber", number.Number, cg.Component
)

_TEMP_NUMBER_SCHEMA = number.number_schema(
    AlpicoolTemperatureNumber,
    unit_of_measurement="°C",
    icon="mdi:thermometer",
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ALPICOOL_ID): cv.use_id(AlpicoolDevice),
        cv.Optional(CONF_TARGET_TEMPERATURE): _TEMP_NUMBER_SCHEMA,
        cv.Optional(CONF_RIGHT_TARGET_TEMPERATURE): _TEMP_NUMBER_SCHEMA,
    }
)


async def _create_number(config, parent, setter, is_right):
    num = await number.new_number(
        config,
        min_value=-20,
        max_value=20,
        step=1,
    )
    cg.add(num.set_parent(parent))
    cg.add(num.set_is_right_zone(is_right))
    cg.add(getattr(parent, setter)(num))


async def to_code(config):
    parent = await cg.get_variable(config[CONF_ALPICOOL_ID])

    if temp_config := config.get(CONF_TARGET_TEMPERATURE):
        await _create_number(temp_config, parent, "set_temperature_number", False)

    if right_temp_config := config.get(CONF_RIGHT_TARGET_TEMPERATURE):
        await _create_number(right_temp_config, parent, "set_right_temperature_number", True)
