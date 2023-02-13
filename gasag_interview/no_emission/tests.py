from django.test import TestCase
from no_emission.models import Emission
# from no_emission.views import

# Create your tests here.


class EmissionTestCase(TestCase):

    def test_url_respond(self):
        import requests
        '''URL Request responds 200'''

        url = "https://umweltbundesamt.api.proxy.bund.dev/api/air_data/v2/measures/json?date_from=%3Cdate_from%3E&"\
            "time_from=%3Chour_from%3E&date_to=%3Cdate_to%3E&time_to=%3Ctime_to%3E&station=129&component=5&scope=2"
        response = requests.get(url)
        status = response.status_code

        self.assertEqual(status, 200)
