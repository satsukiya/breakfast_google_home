from gtts import gTTS
import datetime
import json
import requests
from bs4 import BeautifulSoup


yobi = ["月","火","水","木","金","土","日"]

def weektimes(src):
	dst = 0
	while 0 < src:
		dst += 1
		src -= 7
	return dst

def whats_garbageday():
	today = datetime.datetime.now()
	today_yobi = yobi[today.weekday()]

	garbage_name = "何もない" + today_yobi + "曜日"
	with open("garbage_schedule.json", "r") as fin:
		gdoc = json.load(fin)
		for key in gdoc:
			if  today_yobi in gdoc[key]["week"]:
				if str(gdoc[key]["week_span"]) == "every":
					garbage_name = gdoc[key]["name"]
				elif weektimes(today.day) in gdoc[key]["week_span"]:
					garbage_name = gdoc[key]["name"]

	return garbage_name

def get_time_sun_rise_set(year, month, day, lat,lng):
    url = 'http://labs.bitmeister.jp/ohakon/api/?'
    payload = {'mode':'sun_moon_rise_set', 'year':year, 'month':month, 'day':day, 'lat':lat, 'lng':lng}
    response = requests.get(url, params=payload)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.sunrise_hm.text, soup.sunset_hm.text


def sunriseset_build(d):
	adress = None
	dst = ""
	with open("adress.json", "r") as fin:
		gdoc = json.load(fin)
		adress = gdoc["adress"][0]

	if adress is not None:
		riseset = get_time_sun_rise_set(d.year,d.month,d.day,adress["lat"],adress["lng"])
		dst = adress["name"]
		dst += "の"
		dst += "日の出は"
		dst += riseset[0]
		dst += "、"
		dst += "日の入りは"
		dst += riseset[1]
		dst += "です。"
	return dst


def build():
	today = datetime.datetime.now()
	message = "おはようございます。今日は"
	message += today.strftime("%Y年%m月%d日")
	message += yobi[today.weekday()] + "曜日"
	message += "です。"
	message += "ゴミ収集は"
	message += whats_garbageday()
	message += "です。"
	message += sunriseset_build(today)
	return message

def main():
        tts = gTTS(text=build(), lang='ja')
        file_name = 'wake_up.mp3'
        parent_path = "/var/www/html/"
        tts.save(parent_path + file_name)

if __name__ == '__main__':
	main()
	