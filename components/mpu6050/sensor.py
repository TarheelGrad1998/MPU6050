import esphome.codegen as cg
from esphome.components import i2c, sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_TEMPERATURE,
    DEVICE_CLASS_TEMPERATURE,
    ICON_BRIEFCASE_DOWNLOAD,
    ICON_SCREEN_ROTATION,
    STATE_CLASS_MEASUREMENT,
    UNIT_CELSIUS,
    UNIT_DEGREE_PER_SECOND,
    UNIT_METER_PER_SECOND_SQUARED,
)

DEPENDENCIES = ["i2c"]

CONF_ACCEL = "accel"
CONF_GYRO = "gyro"

mpu6050_ns = cg.esphome_ns.namespace("mpu6050")
MPU6050Component = mpu6050_ns.class_(
    "MPU6050Component", cg.PollingComponent, i2c.I2CDevice
)

accel_schema = sensor.sensor_schema(
    unit_of_measurement=UNIT_METER_PER_SECOND_SQUARED,
    icon=ICON_BRIEFCASE_DOWNLOAD,
    accuracy_decimals=4,
    state_class=STATE_CLASS_MEASUREMENT,
)
gyro_schema = sensor.sensor_schema(
    unit_of_measurement=UNIT_DEGREE_PER_SECOND,
    icon=ICON_SCREEN_ROTATION,
    accuracy_decimals=4,
    state_class=STATE_CLASS_MEASUREMENT,
)
temperature_schema = sensor.sensor_schema(
    unit_of_measurement=UNIT_CELSIUS,
    accuracy_decimals=1,
    device_class=DEVICE_CLASS_TEMPERATURE,
    state_class=STATE_CLASS_MEASUREMENT,
)

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(MPU6050Component),
            cv.Optional(CONF_ACCEL): accel_schema,
            cv.Optional(CONF_GYRO): gyro_schema,
            cv.Optional(CONF_TEMPERATURE): temperature_schema,
        }
    )
    .extend(cv.polling_component_schema("1s"))
    .extend(i2c.i2c_device_schema(0x68))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    accel_key = f"accel"
    if accel_key in config:
        sens = await sensor.new_sensor(config[accel_key])
        cg.add(getattr(var, f"set_accel_sensor")(sens))
    accel_key = f"gyro"
    if accel_key in config:
        sens = await sensor.new_sensor(config[accel_key])
        cg.add(getattr(var, f"set_gyro_sensor")(sens))

    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(sens))
