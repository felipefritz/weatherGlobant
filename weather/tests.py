from django.test import TestCase


class UtilsTest(TestCase):
    pass


class ApiViewsTestCase(TestCase):
    def test_api_loads_properly(self):
        """The weather api loads properly"""
        response = self.client.get('http://127.0.0.1:8000/api/weather/')
        self.assertEqual(response.status_code, 200)

    def test_api_return_location_name_properly(self):
        properly_val = "Santiago, CL"
        headers =  {'Content-Type': 'application/json'}
        response = self.client.get('http://127.0.0.1:8000/api/weather/?city=santiago&country=cl', headers=headers)
        data = response.json()
        print(data)
        self.assertEqual(data['location_name'], properly_val)