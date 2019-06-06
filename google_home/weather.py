import requests
import json

import urllib.parse

from datetime import datetime, date, timedelta

class Weather():
	__CHECK_POINT_COUNT__ = 8
	__WEATHER_API_URL__ = "http://api.openweathermap.org/data/2.5/forecast?"

	def __init__(self, lat, lng):
		self.__lat = lat
		self.__lng = lng
		self.__raw_json_data = self.request_api()
		self.__temparature_list = self.get_temparature_list()

	def request_api(self):
		param_dic = {"units":"metric",
					"lat":self.__lat, 
					"lon":self.__lng, 
					"APPID":"5badbf96c06959340e646241609c575d"}
		param = urllib.parse.urlencode(param_dic)

		url = self.__WEATHER_API_URL__ + param
		response = requests.get(url)
		return response.json()

	def get_temparature_list(self):
		dst = []
		for forcast in self.__raw_json_data["list"][:self.__CHECK_POINT_COUNT__]:
			loc = datetime.fromtimestamp(forcast["dt"])
			dst.append(forcast["main"]["temp"])
		return dst

	@property	
	def max_temperature(self):
		dst = None
		if 0 < len(self.__temparature_list):
			dst = max(self.__temparature_list)
		return dst

	@property
	def min_temperature(self):
		dst = None
		if 0 < len(self.__temparature_list):
			dst = min(self.__temparature_list)
		return dst

	@property
	def weather_at_time(self, hour=12):
		dst = None
		for forcast in self.__raw_json_data["list"][:self.__CHECK_POINT_COUNT__]:
			loc = datetime.fromtimestamp(forcast["dt"])
			if loc.hour == hour:
				dst = forcast["weather"][0]["description"]
		return dst


if __name__ == '__main__':
	with open("adress.json", "r") as fin:
		geo = json.load(fin)
		for city in geo["adress"]:
			print(city["name"])
		#citys= list(map(lambda x: x["name_eng"], geo["adress"]))
		#for c in citys:
			#x = list(filter(lambda x: x["name_eng"] == c,  geo["adress"]))[0]
			#w = Weather(x["lat"], x["lng"])

			#print("max_temp:{}".format(w.max_temperature))
			#print("min_temperature:{}".format(w.min_temperature))
			#print("weather_at_time:{}".format(w.weather_at_time))
