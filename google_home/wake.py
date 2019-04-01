import pychromecast
import sys

def main(http_link):
	chromecasts = pychromecast.get_chromecasts()
	google_home = chromecasts[0]

	google_home.wait()
	mc = google_home.media_controller
	mc.play_media(http_link,'audio/mp3')
	mc.block_until_active()

if __name__ == '__main__':
	args = sys.argv
	if len(args) == 2:
		main(args[1])
	else :
		print("[usage] you should command a link.")
	