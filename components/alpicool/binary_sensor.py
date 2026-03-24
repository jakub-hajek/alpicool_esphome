import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from . import CONF_ALPICOOL_ID, AlpicoolDevice

CONF_CONNECTED = "connected"
CONF_RUNNING = "running"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ALPICOOL_ID): cv.use_id(AlpicoolDevice),
        cv.Optional(CONF_CONNECTED): binary_sensor.binary_sensor_schema(
            device_class="connectivity",
        ),
        cv.Optional(CONF_RUNNING): binary_sensor.binary_sensor_schema(
            device_class="running",
            icon="mdi:snowflake",
        ),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_ALPICOOL_ID])

    if connected_config := config.get(CONF_CONNECTED):
        sens = await binary_sensor.new_binary_sensor(connected_config)
        cg.add(parent.set_connected_binary_sensor(sens))

    if running_config := config.get(CONF_RUNNING):
        sens = await binary_sensor.new_binary_sensor(running_config)
        cg.add(parent.set_running_binary_sensor(sens))
