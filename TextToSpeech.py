from yandex_speech import TTS

#Yandex Speechkit
def t_to_s(text):
	if (len(text)>500): text = text[0:490]
	tts = TTS("oksana", "opus", "b04291f2-5e31-4c8e-af57-1695b7bd5f16", lang="ru_RU", emotion="good")
	tts.generate(text)
	tts.save("ramazan")
	return "ramazan"
