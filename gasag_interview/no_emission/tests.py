from django.test import TestCase
from no_emission.models import Emission
import requests

# Create your tests here.


class EmissionTestCase(TestCase):

    def test_url_respond(self):
        '''URL Request responds 200'''

        url = "https://umweltbundesamt.api.proxy.bund.dev/api/air_data/v2/measures/json?date_from=%3Cdate_from%3E&"\
            "time_from=%3Chour_from%3E&date_to=%3Cdate_to%3E&time_to=%3Ctime_to%3E&station=129&component=5&scope=2"
        response = requests.get(url)
        status = response.status_code

        self.assertEqual(status, 200)

    def test_last_object(self):
        '''gets last emission value, stores in DB and checks if the same'''
        from datetime import datetime, timedelta

        date_from_str = (datetime.now()-timedelta(hours=0)
                         ).strftime("%Y-%m-%d")
        date_to_str = datetime.now().strftime("%Y-%m-%d")
        # format the datetime
        i = 3
        time_from_str = str(datetime.now().hour-i)
        time_to_str = str(datetime.now().hour-i)
        # url
        date_from = date_from_str
        time_from = time_from_str
        date_to = date_to_str
        time_to = time_to_str
        station = "129"
        url = "https://umweltbundesamt.api.proxy.bund.dev/api/air_data/v2/airquality/json?"\
            "date_from="+date_from+"&time_from="+time_from+"&date_to=" + \
            date_to+"&time_to="+time_to+"&station="+station
        print(url)
        # response from request
        response = requests.get(url)
        json_data = response.json()
        json_time_dic = str(datetime.now().replace(
            microsecond=0, second=0, minute=0)-timedelta(hours=i+1))
        print(json_time_dic)
        # Extract NO emission value
        NO_value = json_data['data'][station][json_time_dic][3][1]

        # save in model if not already existing (get_or_create checks if datetime already exists)
        json_time_save = str(datetime.now().replace(
            microsecond=0, second=0, minute=0)-timedelta(hours=0))
        obj = Emission.objects.create(time_date=json_time_save,
                                      emission=NO_value,
                                      station_id=station)
        obj.save()

        load_data = Emission.objects.all().order_by('-time_date')

        # Check time_date
        self.assertEqual(load_data[0].time_date, json_time_save)
        # Check emission value
        self.assertEqual(load_data[0].emission, NO_value)
        # Check station id
        self.assertEqual(load_data[0].station_id, int(station))


# if __name__ == '__main__':
#     unittest.main()
