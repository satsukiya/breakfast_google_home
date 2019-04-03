from gtts import gTTS
import datetime
import json
import requests
from bs4 import BeautifulSoup
import random
from pydub import AudioSegment
import sys

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

def toOlympic():
    now = datetime.datetime.now()
    oly = dt(2020,7,24, 20, 0)
    td = oly - now
    return td.days

def goto2020():
	dst = "東京オリンピック・パラリンピックまであと"
	dst +=  str(toOlympic) + "日です。"

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
	message += goto2020()
	return message

def pageToMarkSoup(url):
	response = requests.get(url)
	return BeautifulSoup(response.content, "html.parser")


def article_link(url):
	archive = pageToMarkSoup(url).find("div", class_="archive-post")
	articles = archive.find_all("div", class_="post-item")
	randindex = random.randint(0, len(articles) - 1)
	return articles[randindex].a["href"]	

def sports():
	alink = article_link("https://www.tokyo-sports.co.jp/entame/")
	aid = alink.split("/")[-2]
	soup = pageToMarkSoup(alink)
	title = soup.find("h1", class_="detail-ttl").text
	article = ""
	contents = soup.find("div", class_="detail-content").find_all("p")
	for item in contents:
		article += item.text

	dst = "東京スポーツの記事を紹介します。\n\n\n"
	dst += title + "\n\n\n" + article
	return dst

def makebot(src, filename="output.mp3", folder="/var/www/html/"):
	tts = gTTS(text=src, lang='ja')
	tts.save(folder + filename)

if __name__ == '__main__':
	args = sys.argv

	if len(args) == 2:
		if args[1] == "0":
			makebot(build(), filename="wake_up.mp3")
		elif args[1] == "1":
			makebot(sports(), filename="article.mp3")
		else :
			print("not type")
	else :
		print("[usage] you should command a message type.")
