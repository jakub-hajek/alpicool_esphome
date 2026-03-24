import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from . import CONF_ALPICOOL_ID, AlpicoolDevice, alpicool_ns

CONF_POWER = "power"
CONF_ECO_MODE = "eco_mode"

AlpicoolPowerSwitch = alpicool_ns.class_("AlpicoolPowerSwitch", switch.Switch, cg.Component)
AlpicoolEcoSwitch = alpicool_ns.class_("AlpicoolEcoSwitch", switch.Switch, cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_ALPICOOL_ID): cv.use_id(AlpicoolDevice),
        cv.Optional(CONF_POWER): switch.switch_schema(
            AlpicoolPowerSwitch,
            icon="mdi:fridge",
        ),
        cv.Optional(CONF_ECO_MODE): switch.switch_schema(
            AlpicoolEcoSwitch,
            icon="mdi:leaf",
        ),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_ALPICOOL_ID])

    if power_config := config.get(CONF_POWER):
        sw = await switch.new_switch(power_config)
        cg.add(sw.set_parent(parent))
        cg.add(parent.set_power_switch(sw))

    if eco_config := config.get(CONF_ECO_MODE):
        sw = await switch.new_switch(eco_config)
        cg.add(sw.set_parent(parent))
        cg.add(parent.set_eco_switch(sw))
