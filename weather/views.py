import requests
from datetime import datetime
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from .utils import kelvin_to_celcius, kelvin_to_fahrenheit


def _get_weather_from__external_api(query: dict):
    """

    :param query: A dictionary with city and country_code as keys.
    :return: A json object with the weather for the specified city
    """
    url = f'https://api.openweathermap.org/data/2.5/weather?q=' \
          f'{query["city"]},' \
          f'{query["country"]}' \
          f'&appid={config("appid")}'

    response = requests.get(url=url)

    if response.status_code == 404:
        return {'error': 'no data available'}

    data = response.json()
    return data


def _build_api_schema(external_weither_data):
    coordinates = list()
    coordinates.append(external_weither_data['coord']['lat'])
    coordinates.append(external_weither_data['coord']['lon'])

    schema = {
        "location_name": "{}, {}".format(external_weither_data['name'], external_weither_data['sys']['country']),
        "temperature": {'celcius': kelvin_to_celcius(external_weither_data['main']['temp']),
                        'fahrenheit': kelvin_to_fahrenheit(external_weither_data['main']['temp'])
                        },
        "wind": external_weither_data['wind'],
        "cloudiness": external_weither_data['weather'][0]['description'],
        "pressure": str(external_weither_data['main']['pressure']) + ' hpa',
        "humidity": str(external_weither_data['main']['humidity']) + '%',
        "sunrise": datetime.utcfromtimestamp(external_weither_data['sys']['sunrise']).strftime('%H:%M'),
        "sunset": datetime.utcfromtimestamp(external_weither_data['sys']['sunset']).strftime('%H:%M'),
        "geo_coordinates": str(coordinates),
        "requested_time": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
        "forecast": ""
    }
    return schema


@api_view(['GET'])
@cache_page(60 * 2)
def get_weather(request):
    """

    This api allows you to get the current weather for any city in the world
    You must specify the following parameters in lowercase:

    country: country code must be the ISO Alpha-2 code, you can find it in:

        https://www.nationsonline.org/oneworld/country_code_list.htm
    city: Name of a valid city

    Usage example:
    http://127.0.0.1:8000/api/weather/?country_code=cl&city=santiago

    """
    query = {'country_code': '', 'city': ''}
    query_params = request.query_params

    if 'country'not in query_params and 'city' not in query_params:
        return Response({'error': 'no valid params detected'},
                        status=status.HTTP_400_BAD_REQUEST)

    elif 'country' not in query_params:
        return Response({'error': 'You must to specify the COUNTRY ISO Alpha-2 code with the param: country_code'},
                        status=status.HTTP_400_BAD_REQUEST)

    elif 'city' not in query_params:
        return Response({'error': 'You must add city as param and the value as a valid city'},
                        status=status.HTTP_400_BAD_REQUEST)

    else:
        query['country'] = request.query_params['country']
        query['city'] = request.query_params['city']

        response_from_api = _get_weather_from__external_api(query)
        response = _build_api_schema(response_from_api)

        return Response(response, status=status.HTTP_200_OK, )





