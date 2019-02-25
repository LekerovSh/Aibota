# _*_ coding: utf-8 _*_
import requests, config, json, base64
from telebot import TeleBot

TELEGRAM_KEY = config.token
bot = TeleBot(TELEGRAM_KEY)
print("Start locale telegram bot")

@bot.message_handler(content_types=['voice'])
def answer_voice(message):
    bot.send_chat_action(message.chat.id, 'typing')
    voice = message.voice
    key = "AIzaSyAmlSnOEVeOhuCpet_lCtxCSXAb3C36VIo"
    file_url = "https://api.telegram.org/file/bot{}/{}".format(
        bot.token,
        bot.get_file(voice.file_id).file_path
    )
    url = "https://speech.googleapis.com/v1/speech:recognize?key={}".format(key)
    headers = {"Content-type": 'application/json'}
    audio_content = str(base64.b64encode(requests.get(file_url).content))
    audio_content = audio_content[:-1]
    audio_content = audio_content[2:]
    payload = {
        "config": {
            "encoding": "OGG_OPUS",
            "languageCode": "ru-RU",
            "sampleRateHertz": 48000
        },
        "audio": {
            "content": audio_content
        }
    }

    res = requests.post(
        url=url,
        data=json.dumps(payload),
        headers=headers
    )
    data = res.json()
    txt = data['results'][0]['alternatives'][0]['transcript']
    print(txt)
    bot.send_message(message.chat.id, txt)


if __name__ == '__main__':
    bot.polling(none_stop=True)
