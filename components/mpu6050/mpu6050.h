#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/i2c/i2c.h"

namespace esphome::mpu6050 {

class MPU6050Component : public PollingComponent, public i2c::I2CDevice {
 public:
  void setup() override;
  void dump_config() override;

  void update() override;

  void set_accel_sensor(sensor::Sensor *accel_sensor) { accel_sensor_ = accel_sensor; }
  void set_temperature_sensor(sensor::Sensor *temperature_sensor) { temperature_sensor_ = temperature_sensor; }
  void set_gyro_sensor(sensor::Sensor *gyro_sensor) { gyro_sensor_ = gyro_sensor; }

 protected:
  sensor::Sensor *accel_sensor_{nullptr};
  sensor::Sensor *temperature_sensor_{nullptr};
  sensor::Sensor *gyro_sensor_{nullptr};
};

}  // namespace esphome::mpu6050
