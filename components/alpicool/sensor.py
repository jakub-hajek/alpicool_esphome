import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_VOLT,
)
from . import CONF_ALPICOOL_ID, AlpicoolDevice

CONF_CURRENT_TEMPERATURE = "current_temperature"
CONF_TARGET_TEMPERATURE = "target_temperature"
CONF_INPUT_VOLTAGE = "input_voltage"
CONF_RIGHT_CURRENT_TEMPERATURE = "right_current_temperature"
CONF_RIGHT_TARGET_TEMPERATURE = "right_target_temperature"

_TEMP_SCHEMA = sensor.sensor_schema(
    unit_of_measurement=UNIT_CELSIUS,
    accuracy_decimals=0,
    device_class=DEVICE_CLASS_TEMPERATURE,
    state_class=STATE_CLASS_MEASUREMENT,
)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ALPICOOL_ID): cv.use_id(AlpicoolDevice),
        cv.Optional(CONF_CURRENT_TEMPERATURE): _TEMP_SCHEMA,
        cv.Optional(CONF_TARGET_TEMPERATURE): _TEMP_SCHEMA,
        cv.Optional(CONF_INPUT_VOLTAGE): sensor.sensor_schema(
            unit_of_measurement=UNIT_VOLT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_VOLTAGE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_RIGHT_CURRENT_TEMPERATURE): _TEMP_SCHEMA,
        cv.Optional(CONF_RIGHT_TARGET_TEMPERATURE): _TEMP_SCHEMA,
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_ALPICOOL_ID])

    for conf_key, setter in [
        (CONF_CURRENT_TEMPERATURE, "set_current_temperature_sensor"),
        (CONF_TARGET_TEMPERATURE, "set_target_temperature_sensor"),
        (CONF_RIGHT_CURRENT_TEMPERATURE, "set_right_current_temperature_sensor"),
        (CONF_RIGHT_TARGET_TEMPERATURE, "set_right_target_temperature_sensor"),
    ]:
        if sens_config := config.get(conf_key):
            sens = await sensor.new_sensor(sens_config)
            cg.add(getattr(parent, setter)(sens))

    if voltage_config := config.get(CONF_INPUT_VOLTAGE):
        sens = await sensor.new_sensor(voltage_config)
        cg.add(parent.set_voltage_sensor(sens))
