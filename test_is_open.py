from locu import VenueApiClient
import sys
import unittest

global KEY


<<<<<<< HEAD
class IsOpenTest(unittest.TestCase):
=======
class IsOpenTest(object):
>>>>>>> 926705451e4d72f635a061e8d36169c1dd49cf28

	def test_no_data(self):
		venue_client = VenueApiClient(KEY)
		venue_id = "50d70de7fbafb112c2de" ##no data
<<<<<<< HEAD
		self.assertIsNone(venue_client.is_open(venue_id,"12:00:00","Monday"))
=======
		self.assertEqual(venue_client.is_open(venue_id,"12:00:00","Monday"))
>>>>>>> 926705451e4d72f635a061e8d36169c1dd49cf28


	def test_open(self):
		venue_client = VenueApiClient(KEY)
		venue_id='b7b1644a6bb10dff58bd' ## open Monday 09:00:00 - 15:00:00
<<<<<<< HEAD
		self.assertTrue(venue_client.is_open(venue_id,"12:00:00","Monday"))
=======
		self,assertTrue(venue_client.is_open(venue_id,"12:00:00","Monday"))
>>>>>>> 926705451e4d72f635a061e8d36169c1dd49cf28


	def test_closed(self):
		venue_client = VenueApiClient(KEY)
		venue_id='b7b1644a6bb10dff58bd' ## open Monday 09:00:00 - 15:00:00
		self.assertFalse(venue_client.is_open(venue_id,"16:00:00","Monday"))



if __name__ == '__main__':
	print "Please enter a locu api key"
	KEY = sys.stdin.readline().strip()
<<<<<<< HEAD
	print KEY
=======
>>>>>>> 926705451e4d72f635a061e8d36169c1dd49cf28
	unittest.main()
