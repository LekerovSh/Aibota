# -*- coding: utf-8 -*-
import config
from telebot import types
import telebot
from weather import weatherapp
from wikiapi import wikiapp

from xml.etree import ElementTree
import requests
from telebot import TeleBot
import uuid
from TextToSpeech import t_to_s
import time

from settings import init

from ruleBasedNER import ner
from chitchat import chat
from datetime import datetime

from yandex_translate import translate
from currency import currencyapp

from youtube import youtube_search

import settings

init()

YANDEX_KEY = 'b04291f2-5e31-4c8e-af57-1695b7bd5f16'
VOICE_LANGUAGE = 'ru-RU'
MAX_MESSAGE_SIZE = 1000 * 50
MAX_MESSAGE_DURATION = 60
bot = telebot.TeleBot(config.token)
print("Start locale telegram bot")

k = types.InlineKeyboardMarkup()
button_data = {}
inweather = types.InlineKeyboardButton(text="Прогноз погоды", callback_data="callback_weather")
inwikipedia = types.InlineKeyboardButton(text="Энциклопедия", callback_data="callback_wikipedia")
incurrency = types.InlineKeyboardButton(text="Конвертор валют", callback_data="callback_currency")
intranslate = types.InlineKeyboardButton(text="Переводчик", callback_data="callback_translate")
inboltun = types.InlineKeyboardButton(text="Болталка", callback_data="callback_bl")
k.add(inweather)
k.add(inwikipedia)
k.add(incurrency)
k.add(intranslate)
k.add(inboltun)

back = types.InlineKeyboardMarkup()
back_button = types.InlineKeyboardButton(text="Список функции", callback_data="callback_back")
back.add(back_button)


@bot.message_handler(commands=['start'])
def for_menu(message):
    bot.send_message(message.chat.id, "Для подробной информации нажмите на кнопку:", reply_markup=k)


def get_answer(user_input, user_date):
    ans = ""
    #####################################################################################################################
    #####################################################################################################################

    name_of_service = "No"  # чтобы определить именно запрос для википедиия я создал эту переменную

    #####################################################################################################################
    #####################################################################################################################

    # write predefined set of questions and answers here
    if user_input == u"Привет":
        ans = u"Привет. Как я могу помочь?"
    elif ('привет' in user_input) or ('как дела' in user_input):
        ans = "Привет! Как ваши дела?"
    elif ('хорошо' in user_input) or ('сама' in user_input):
        ans = "Рада это слышать. У меня тоже все хорошо"
    elif user_input == "/text":
        ans = "Задайте мне любую из команд в моем списке. Я постараюсь выполнить или можем просто поговорить.\n- Какая сегодня погода в Алмате?\n- Расскажи о Казахстане\n- Переведи слово кофе на английский\n- 2 доллара в тенге\n- Давай поболтаем, AIbota\n* Чтобы воспользоваться голосовым помощником, отправьте аудиозапрос.\n"
    elif ('умеешь' in user_input) or ('умеешь делать' in user_input):
        ans = 'Вот что я умею:\n- Показать прогноз погоды\n("Какая сегодня погода в Алмате?") ' + u'⛅' + '\n- Рассказать интересные факты\n("Расскажи о Казахстане") ' + u'🔍' + '\n- Переводить слова\n("кофе на английском") ' + u'🔄' + '\n- Узнавать курсы валют\n("доллары в тенге") ' + u'💲' + '\n- Составить компанию\n("Давай поболтаем, AIbota") ' + u'💬' + "\n* Чтобы воспользоваться голосовым помощником, отправьте аудиозапрос " + u'📣' + ".\n"
    elif (user_input == '/info') or (
            'подробнее о функциях' in user_input or 'о своих функциях' in user_input or 'о своих функциях' in user_input):
        ans = "С помощью этого бота вы можете\n [ " + u'📣' + " ] - Воспользоваться персональной голосовой помощницей, отправляя аудио запросы\n [ " + u'⛅' + " Прогноз погоды] - Узнавать погоду на сегодня(ближайщий час), завтра, послезавтра в любом городе\n [ " + u'🔍' + " Энциклопедия] - Получать информацию из энциклопедии\n [ " + u'🔄' + " Переводчик] - Переводить слова\n [ " + u'💲' + " Конвертер валют] - Узнавать курсы валют\n [ " + u'💬' + " Болталка] - Или просто поболтать\n"
    else:
        serv = ner(user_input)
        print(serv[0])

        if serv[0] == "weather":
            settings.context["service"] = "weather"
            [service, city, date] = ner(user_input)
            # [service, city, date] = ner(user_input)
            #ans="connct to the api: " + service + " " + " " + city + " " + date

            ans = weatherapp(city, date, user_date)[1]
            print(city)

            if ans == "error":
                ans = "К сожалению места с таким именем не найдено, проверьте имя места и попробуйте снова"
            name_of_service = "weather"  # если это погода возвращаю имя сервиса
            return ans, name_of_service

        if (settings.context["service"] == "weather" and ("завтра" in user_input)):
            settings.context["service"] = "weather"
            [service, city, date] = [settings.context["service"], settings.context["city"], "завтра"]
            # [service, city, date] = ner(user_input)
            ans = "connct to the api: " + service + " " + " " + city + " " + date
            ans = weatherapp(city, date, user_date)[1]
            print(city)
            if ans == "error":
                ans = "К сожалению места с таким именем не найдено, проверьте имя места и попробуйте снова"
            name_of_service = "weather"  # если это погода возвращаю имя сервиса
            return ans, name_of_service
        if serv[0] == "translate":
            settings.context["service"] = "translate"
            [service, textToTranslate, finalLangToTranslate] = ner(user_input)
            ans = translate("", finalLangToTranslate, textToTranslate)
            name_of_service = "translate"  # если это переводчик возвращаю имя сервиса
            return ans, name_of_service
        if serv[0] == "currency":
            settings.context["service"] = "currency"
            [service, finalFirstCurr, finalSecondCurr, curr] = ner(user_input)
            ans = currencyapp(finalFirstCurr, finalSecondCurr, curr)
            name_of_service = "currency"  # если это конвертор валют возвращаю имя сервиса
            return ans, name_of_service
        if serv[0] == "wiki":
            settings.context["service"] = "wiki"
            [service, query] = ner(user_input)
            print(query)
            ans = wikiapp(query)
            name_of_service = query + "serviceapiwikipedia"  # если это википедия возвращаю имя сервиса
            return ans, name_of_service
        if serv[0] == "youtube":
            settings.context["service"] = "youtube"
            [service, result] = ner(user_input)
            print(result)
            ans = youtube_search(result)
            name_of_service = "youtube"  # если это википедия возвращаю имя сервиса
            return ans, name_of_service
        if serv == "chitchat" and ans == "":
            settings.context["service"] = "chitchat"
            ans = chat(user_input)
            name_of_service = "chitchat"  # если это болталка возвращаю имя сервиса
            return ans, name_of_service
    return ans, name_of_service

def get_answer_for_voice(user_input, user_date):
    ans = []
    name_of_service = "No"
    # write predefined set of questions and answers here
    if user_input == u"Привет":

        ans = [u"Привет. Как я могу помочь?", u"Привет. Как я могу помочь?"]
    elif ('привет' in user_input) or ('как дела' in user_input):
        ans = ["Привет! Как ваши дела?", "Привет! Как ваши дела?"]
    elif ('хорошо' in user_input) or ('сама' in user_input):
        ans = ["Рада это слышать. У меня тоже все хорошо", "Рада это слышать. У меня тоже все хорошо"]
    elif user_input == "/start":
        ans = [
            "Задайте мне любую из команд в моем списке. Я постараюсь выполнить или можем просто поговорить.\n- Какая сегодня погода в Алмате?\n- Расскажи о Казахстане\n- Переведи слово кофе на английский\n- 2 доллара в тенге\n- Давай поболтаем, AIbota\n* Чтобы воспользоваться голосовым помощником, отправьте аудиозапрос.\n",
            "Задайте мне любую из команд в моем списке. Я постараюсь выполнить или можем просто поговорить.\n- Какая сегодня погода в Алмате?\n- Расскажи о Казахстане\n- Переведи слово кофе на английский\n- 2 доллара в тенге\n- Давай поболтаем, AIbota\n* Чтобы воспользоваться голосовым помощником, отправьте аудиозапрос.\n"]
    elif ('умеешь' in user_input) or ('умеешь делать' in user_input):
        ans = [
            'Вот что я умею:\n- Показать прогноз погоды\n("Какая сегодня погода в Алмате?") ' + u'⛅' + '\n- Рассказать интересные факты\n("Расскажи о Казахстане") ' + u'🔍' + '\n- Переводить слова\n("кофе на английском") ' + u'🔄' + '\n- Узнавать курсы валют\n("доллары в тенге") ' + u'💲' + '\n- Составить компанию\n("Давай поболтаем, AIbota") ' + u'💬' + "\n* Чтобы воспользоваться голосовым помощником, отправьте аудиозапрос " + u'📣' + ".\n",
            'Вот что я умею:\n- Показать прогноз погоды\n("Какая сегодня погода в Алмате?") ' + u'⛅' + '\n- Рассказать интересные факты\n("Расскажи о Казахстане") ' + u'🔍' + '\n- Переводить слова\n("кофе на английском") ' + u'🔄' + '\n- Узнавать курсы валют\n("доллары в тенге") ' + u'💲' + '\n- Составить компанию\n("Давай поболтаем, AIbota") ' + u'💬' + "\n* Чтобы воспользоваться голосовым помощником, отправьте аудиозапрос " + u'📣' + ".\n"]
    elif (user_input == '/info') or (
            'подробнее о функциях' in user_input or 'подробней о функциях' in user_input or 'функциях' in user_input or 'о своих функциях' in user_input or 'о своих функциях' in user_input):
        ans = [
            "С помощью этого бота вы можете\n [ " + u'📣' + " ] - Воспользоваться персональной голосовой помощницей, отправляя аудио запросы\n [ " + u'⛅' + " Прогноз погоды] - Узнавать погоду на сегодня(ближайщий час), завтра, послезавтра в любом городе\n [ " + u'🔍' + " Энциклопедия] - Получать информацию из энциклопедии\n [ " + u'🔄' + " Переводчик] - Переводить слова\n [ " + u'💲' + " Конвертер валют] - Узнавать курсы валют\n [ " + u'💬' + " Болталка] - Или просто поболтать\n",
            "С помощью этого бота вы можете\n [ " + u'📣' + " ] - Воспользоваться персональной голосовой помощницей, отправляя аудио запросы\n [ " + u'⛅' + " Прогноз погоды] - Узнавать погоду на сегодня(ближайщий час), завтра, послезавтра в любом городе\n [ " + u'🔍' + " Энциклопедия] - Получать информацию из энциклопедии\n [ " + u'🔄' + " Переводчик] - Переводить слова\n [ " + u'💲' + " Конвертер валют] - Узнавать курсы валют\n [ " + u'💬' + " Болталка] - Или просто поболтать\n"]
    else:
        serv = ner(user_input)
        print(serv[0])
        if (settings.context["service"] == "weather" and ("завтра" in user_input)):
            settings.context["service"] = "weather"
            [service, city, date] = [settings.context["service"], settings.context["city"], "завтра"]

            # [service, city, date] = ner(user_input)
            # ans="connct to the api: " + service + " " + " " + city + " " + date

            ans = weatherapp(city, date, user_date)
            print(city)
            if ans[0] == "error":
                ans = ["К сожалению места с таким именем не найдено, проверьте имя места и попробуйте снова",
                       "К сожалению места с таким именем не найдено, проверьте имя места и попробуйте снова"]
            name_of_service = "weather"
            return ans, name_of_service
        if serv[0] == "weather":
            settings.context["service"] = "weather"
            [service, city, date] = ner(user_input)
            # [service, city, date] = ner(user_input)
            # ans="connct to the api: " + service + " " + " " + city + " " + date

            ans = weatherapp(city, date, user_date)

            print(city)
            if ans[0] == "error":
                ans = ["К сожалению места с таким именем не найдено, проверьте имя места и попробуйте снова",
                       "К сожалению места с таким именем не найдено, проверьте имя места и попробуйте снова"]
            name_of_service = "weather"
            return ans, name_of_service
        if serv[0] == "translate":
            [service, textToTranslate, finalLangToTranslate] = ner(user_input)
            ans = translate("", finalLangToTranslate, textToTranslate)
            name_of_service = "translate"
            return [ans, ans], name_of_service
        if serv[0] == "currency":
            settings.context["service"] = "currency"
            [service, finalFirstCurr, finalSecondCurr, curr] = ner(user_input)
            ans = currencyapp(finalFirstCurr, finalSecondCurr, curr)
            name_of_service = "currency"
            return [ans, ans], name_of_service
        if serv[0] == "wiki":
            settings.context["service"] = "wiki"
            [service, query] = ner(user_input)
            print(query)
            ans = wikiapp(query)
            name_of_service = query + "serviceapiwikipedia"
            return [ans, ans], name_of_service
        if serv[0] == "youtube":
            settings.context["service"] = "youtube"
            [service, result] = ner(user_input)
            print(result)
            ans = youtube_search(result)
            name_of_service = "youtube"  # если это википедия возвращаю имя сервиса
            return [ans, ans], name_of_service
        if serv == "chitchat" or ans == "":
            settings.context["service"] = "chitchat"
            ans = chat(user_input)
            name_of_service = "chitchat"
            return [ans, ans], name_of_service
    return ans, name_of_service


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    user_input = message.text
    ans = ""
    
    bot.send_chat_action(message.chat.id, 'typing')

    user_date = datetime.fromtimestamp(int(message.date))
    #ans = youtube_search(message.text)
    #bot.send_message(message.chat.id, ans, parse_mode="HTML")

    [ans, name_of_service] = get_answer(user_input, user_date)
    print("Name of service:" + name_of_service)

    if 'serviceapiwikipedia' in name_of_service:  # если имя сервиса будет википедия
        search_text = name_of_service[:-19]
        wiki_keyboard = types.InlineKeyboardMarkup()  # создаю для него клавиатуру
        wiki_key_more = types.InlineKeyboardButton(text="Подробнее",
                                                   callback_data=search_text + " serviceapiwikipedia")  # создаю клавиш
        wiki_keyboard.add(wiki_key_more)  # добавляю клавиш на нашу клавиатуру
        wiki_keyboard.add(back_button)
        info = (ans[:200] + '...') if len(ans) > 75 else ans  # сокращаю длину ответа из википедии до 200 символов
        bot.send_message(message.chat.id, text=info,
                         reply_markup=wiki_keyboard)  # отправляю наше сообщение и клавиатуру
    else:
        bot.send_message(message.chat.id, ans, parse_mode="HTML", reply_markup=back)

    

@bot.message_handler(content_types=["voice"])
def voice_messages(message):
    data = message.voice

    ans = []

    bot.send_chat_action(message.chat.id, 'typing')

    user_date = datetime.fromtimestamp(int(message.date))

    if (data.file_size > MAX_MESSAGE_SIZE) or (data.duration > MAX_MESSAGE_DURATION):
        reply = ' '.join((
            "Голосовое сообщение слишком длинное.",
            "Максимальная длительность: {} сек.".format(MAX_MESSAGE_DURATION),
            "Постарайтесь говорить по короче.",
        ))
        return bot.reply_to(message, reply)
    file_url = "https://api.telegram.org/file/bot{}/{}".format(
        bot.token,
        bot.get_file(data.file_id).file_path
    )
    xml_data = requests.post(
        "https://asr.yandex.net/asr_xml?uuid={}&key={}&topic={}&lang={}".format(
            uuid.uuid4().hex,
            YANDEX_KEY,
            'queries',
            VOICE_LANGUAGE
        ),
        data=requests.get(file_url).content,
        headers={"Content-type": 'audio/ogg;codecs=opus'}
    ).content

    e_tree = ElementTree.fromstring(xml_data)

    if not int(e_tree.attrib.get('success', '0')):
        mess = "Говорите кратко и ясно, а то Вас плохо слышно"
        t_to_s(mess)
        voice = open('ramazan.opus', 'rb')
        return bot.send_voice(message.chat.id, voice), bot.send_message(message.chat.id, mess)

    text = e_tree[0].text
    print(text)
    if ('<censored>' in text) or (not text):
        mess = "Не понял, пожалуйста повторите"
        t_to_s(mess)
        voice = open('ramazan.opus', 'rb')
        return bot.send_voice(message.chat.id, voice), bot.send_message(message.chat.id, mess)
    user_input = text
    [ans, name_of_service] = get_answer_for_voice(user_input, user_date)
    mess = ans[0]
    txt = ans[1]

    print(txt)
    t_to_s(mess)
    voice = open('ramazan.opus', 'rb')
    if 'serviceapiwikipedia' in name_of_service:  # если имя сервиса будет википедия
        search_text = name_of_service[:-19]
        wiki_keyboard = types.InlineKeyboardMarkup()  # создаю для него клавиатуру
        wiki_key_more = types.InlineKeyboardButton(text="Подробнее",
                                                   callback_data=search_text + " serviceapiwikipedia")  # создаю клавиш
        wiki_keyboard.add(wiki_key_more)  # добавляю клавиш на нашу клавиатуру
        wiki_keyboard.add(back_button)
        info = (mess[:200] + '...') if len(txt) > 75 else txt  # сокращаю длину ответа из википедии до 200 символов
        return bot.send_voice(message.chat.id, voice), bot.send_message(message.chat.id, info, parse_mode="HTML",
                                                                        reply_markup=wiki_keyboard)
    else:
        return bot.send_voice(message.chat.id, voice), bot.send_message(message.chat.id, ans[1], parse_mode="HTML",
                                                                        reply_markup=back)


'''    
############################################################################################
    if('привет' in text) or ('как дела' in text):
        mess ="Привет! Как ваши дела?"
        t_to_s(mess)
        voice = open('ramazan.opus', 'rb')
        return bot.send_voice(message.chat.id, voice), bot.send_message(message.chat.id,mess)

    if('хорошо' in text) or ('сама' in text):
        mess ="Рада это слышать. У меня тоже все хорошо"
        t_to_s(mess)
        voice = open('ramazan.opus', 'rb')
        return bot.send_voice(message.chat.id, voice), bot.send_message(message.chat.id,mess)
#####################################################################################################
    mess ="Такса едет в такси. Такса едет в такси. Такса едет в такси. Такса едет в такси. Все приехали, мерси."
    t_to_s(mess)
    voice = open('ramazan.opus', 'rb')
    return bot.send_voice(message.chat.id, voice), bot.send_message(message.chat.id,mess)
'''


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "callback_back":
            bot.send_message(chat_id=call.message.chat.id,
                             text="Для подробной информации нажмите на кнопку:", reply_markup=k)
        elif call.data == "callback_weather":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="<i>Бот понимает человеческий язык, поэтому вы можете узнать погоду в виде вопросов.</i>"
                                       + "\n\nВы можете написать или отправить голосовое сообщение  в виде  вопросов такого формата:"
                                       + "\n\n<b>Погода в Астане?</b>"
                                       + "\n\n<b>Погода на сегодня в Астане?</b>"
                                       + "\n\n<b>Погода на завтра в Астане?</b>"
                                       + "\n\n<b>Погода на послезавтра в Астане?</b>"
                                       + "\n\n<b>Расскажи про погоду  в Астане на сегодня?</b>",
                                  parse_mode="HTML", reply_markup=back)
        elif call.data == "callback_wikipedia":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="<i>Бот понимает человеческий язык, поэтому вы можете спросить у него интересующий вам вопрос.</i>" +
                                       "\n\nВы можете написать или отправить голосовое сообщение  в виде  вопросов такого формата:" +
                                       "\n\n<b>Расскажи о Элизавет Тейлор?</b>" +
                                       "\n\n<b>Что такой копирайтинг?</b>" +
                                       "\n\n<b>Расскажи о Казахстане</b>" +
                                       "\n\n<b>Что означает слово 'склонность'?</b>",
                                  parse_mode="HTML", reply_markup=back)
        elif call.data == "callback_currency":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="<i>Бот понимает человеческий язык, поэтому чтобы конвертировать валюты вы можете спросить у нее об этом.</i>" +
                                       "\n\nВы можете написать или отправить голосовое сообщение  в виде  вопросов такого формата:" +
                                       "\n\n<b>20 доллар в тенге?</b>" +
                                       "\n\n<b>Сколько будет 30 евро в долларах?</b>" +
                                       "\n\n<b>Сколько будет 100 рубль в марках</b>" +
                                       "\n\n<b>1 биткоин в долларах?</b>" +
                                       "\n\n<b>300 сом в тенге?</b>",
                                  parse_mode="HTML", reply_markup=back)
        elif call.data == "callback_translate":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="<i>Бот понимает человеческий язык, поэтому вы можете переводить слова и тексты просто спросив об этом у нее.</i>" +
                                       "\n\nВы можете написать или отправить голосовое сообщение  в виде  вопросов такого формата:" +
                                       "\n\n<b>'Космос' на английском?</b>" +
                                       "\n\n<b>Как переводится available на казахском языке?</b>" +
                                       "\n\n<b>Как переводится где находится аптека? на китайском языке?</b>" +
                                       "\n\n<b>Переведи слово разочаровываешь на казахский язык?</b>",
                                  parse_mode="HTML", reply_markup=back)
        elif call.data == "callback_bl":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="<i>Особенностью этого бота является то, что оно понимает человеческий язык. </i>" +
                                       "\n\n<b>Если вы хотите просто поговорить с ботом напишите ему  'Давай поболтаем'.</b>",
                                  parse_mode="HTML", reply_markup=back)
        ############################################################################################################
        ############################################################################################################
        ############################################################################################################
        elif 'serviceapiwikipedia' in call.data:
            more = call.data[:-19]
            r = wikiapp(more)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=r, reply_markup=back)
        ############################################################################################################
        ############################################################################################################
        ####################################    ########################################################################
        ############################################################################################################


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as err:
        print("Разорвано интернет соединение")
