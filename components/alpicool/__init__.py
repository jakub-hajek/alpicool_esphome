import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import ble_client
from esphome.const import CONF_ID

CODEOWNERS = ["@zamek"]
DEPENDENCIES = ["ble_client"]
AUTO_LOAD = ["sensor", "binary_sensor", "switch", "number"]
MULTI_CONF = True

CONF_ALPICOOL_ID = "alpicool_id"

alpicool_ns = cg.esphome_ns.namespace("alpicool")
AlpicoolDevice = alpicool_ns.class_(
    "AlpicoolDevice", cg.PollingComponent, ble_client.BLEClientNode
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(AlpicoolDevice),
        }
    )
    .extend(cv.polling_component_schema("2s"))
    .extend(ble_client.BLE_CLIENT_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await ble_client.register_ble_node(var, config)
