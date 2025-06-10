import bme680


try:
    sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
except (RuntimeError, IOError):
    sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
    
    

# calibrare
for name in dir(sensor.calibration_data):

    if not name.startswith('_'):
        value = getattr(sensor.calibration_data, name)

#        if isinstance(value, int):
#            print('{}: {}'.format(name, value))


sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)
sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)



for name in dir(sensor.data):
    value = getattr(sensor.data, name)

#    if not name.startswith('_'):
#        print('{}: {}'.format(name, value))

sensor.set_gas_heater_temperature(320)
sensor.set_gas_heater_duration(250)
#sensor.select_gas_heater_profile(0)

# Up to 10 heater profiles can be configured, each
# with their own temperature and duration.
#sensor.set_gas_heater_profile(200, 150, nb_profile=1)
#sensor.set_gas_heater_profile(200, 150, nb_profile=1)
#sensor.select_gas_heater_profile(1)
#sensor.data.heat_stable = True


def read_temp()->float | None:
    """Read temp."""
    sensor.select_gas_heater_profile(1)
    if sensor.get_sensor_data():
        return round(sensor.data.temperature, 2)
    return None

def read_pressure()->float | None:
    """Read the pressure"""
    sensor.select_gas_heater_profile(1)
    if sensor.get_sensor_data():
        return round(sensor.data.pressure, 2)
    return None
    
def read_hum()->float | None:
    """Read the humidity"""
    sensor.select_gas_heater_profile(1)
    if sensor.get_sensor_data():
        return round(sensor.data.humidity, 2)
    return None
    
#def read_gas()->float | None:
#    """Read gas resistance"""
##    print(f"heat_stable: {sensor.data.heat_stable}")
#    sensor.set_gas_heater_profile(200, 150, nb_profile=1)
#    if sensor.get_sensor_data() and sensor.data.heat_stable:
#        return sensor.data.gas_resistance
#    return None