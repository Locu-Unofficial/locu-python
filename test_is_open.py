from locu import VenueApiClient
import sys
import unittest

global KEY


class IsOpenTest(object):

	def test_no_data(self):
		venue_client = VenueApiClient(KEY)
		venue_id = "50d70de7fbafb112c2de" ##no data
		self.assertEqual(venue_client.is_open(venue_id,"12:00:00","Monday"))


	def test_open(self):
		venue_client = VenueApiClient(KEY)
		venue_id='b7b1644a6bb10dff58bd' ## open Monday 09:00:00 - 15:00:00
		self,assertTrue(venue_client.is_open(venue_id,"12:00:00","Monday"))


	def test_closed(self):
		venue_client = VenueApiClient(KEY)
		venue_id='b7b1644a6bb10dff58bd' ## open Monday 09:00:00 - 15:00:00
		self.assertFalse(venue_client.is_open(venue_id,"16:00:00","Monday"))



if __name__ == '__main__':
	print "Please enter a locu api key"
	KEY = sys.stdin.readline().strip()
	unittest.main()
