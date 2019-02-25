import requests

def translate(lang_from, lang_to, text):
    yandex_translate_api_key = "trnsl.1.1.20180722T152305Z.6490b9bee1c4635f.1afe541a71f20251650f259a9c178b21d7489307"
    res = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate",
                       params={'key': yandex_translate_api_key, 'lang': lang_to, 'text': text})
    data = res.json()
    if (data['code'] == 200):
        translating_text = text + " - " + data['text'][0]
    else:
        translating_text = "Error!"
    return translating_text

'''lang_from = ""
lang_to = "ru"
s = input()

print(translate(lang_from, lang_to, s))'''
