
KELVIN = 273.15


def kelvin_to_celcius(kelvin_value):
    celcius = kelvin_value - KELVIN
    return int(celcius)


def kelvin_to_fahrenheit(kelvin_value):
    fahrenheit = ((kelvin_value - 273.15) * 1.8) + 32
    return int(fahrenheit)