import pychromecast

def main():
	http_link = "http://localhost/wake_up.mp3"
	chromecasts = pychromecast.get_chromecasts()
	google_home = chromecasts[0]

	google_home.wait()
	mc = google_home.media_controller
	mc.play_media(http_link,'audio/mp3')
	mc.block_until_active()

if __name__ == '__main__':
	main()
	