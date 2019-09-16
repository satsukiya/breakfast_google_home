import pychromecast
import sys
import netifaces as ni

def localaddress():
	return ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']


def main(music_title):
	chromecasts = pychromecast.get_chromecasts()
	google_home = chromecasts[0]

	google_home.wait()
	http_link = "http://{0}/{1}".format(localaddress(), music_title)
	mc = google_home.media_controller
	mc.play_media(http_link,'audio/mp3')
	mc.block_until_active()

if __name__ == '__main__':
	args = sys.argv
	if len(args) == 2:
		main(args[1])
	else :
		print("[usage] you should command a link.")
