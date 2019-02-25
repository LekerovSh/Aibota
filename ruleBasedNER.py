import re
import string
import settings
from lang import langList
import requests


def ner(uinput):
    
    us = uinput
    translator = str.maketrans('', '', string.punctuation)
    #check for weather service keywords
    us =us.translate(translator).lower()
    s = us
    slist = s.split(" ")
    s = " ".join(slist)  
    stop_words = ["какая", "какой", "какие", "покажи","пожалуйста","расскажи"]
    for word in stop_words:
        if (s.find(word)>=0):
            s = s.replace(word, "")
    service = ""
    city = settings.context["city"]
    date = settings.context["date"]
    #TODO: код чтобы находить даты нужно написать со следующей строки, описание дано снизу

    # находит слово на дату, выводит их и удалет из строки
    # например: дана строка s равная "расскажи погоду% на сегодня% в алматы"
    # он выводит date: сегодня, и удаляет подстроку с датой(это может быть любое название даты) " на сегодня"(с первым пробелом), 
    # в конце остается строка s как "расскажи погоду в алматы"
    # и можно его дальше передавать, чтобы он распознал сервис и город

    date1 = '[\w+\s[на\s]?]?сегодня'
    date2 = '[\w+\s[на\s]?]?завтра'
    date3 = '[\w+\s[на\s]?]?послезавтра'

    sam = []
    good = False

    m = re.search(date1, s)
    if m:
        date = "сегодня"
    m = re.search(date2, s)
    if m:
        date = "завтра"
    m = re.search(date3, s)
    if m:
        date = "послезавтра"

    # print (date)

    sample = '.*[\w+\s[на\s]?]?завтра.*'
    samp = re.search(sample, s)
    if samp:
        good = True
        sam = samp.group(0)
        sam = sam.split(' ')
        if 'на' in sam:
            sam.remove('на')
        if 'завтра' in sam:
            sam.remove('завтра')

    sample = '.*[\w+\s[на\s]?]?сегодня.*'
    samp = re.search(sample, s)
    if samp:
        good = True
        sam = samp.group(0)
        sam = sam.split(' ')
        if 'на' in sam:
            sam.remove('на')
        if 'сегодня' in sam:
            sam.remove('сегодня')

    sample = '.*[\w+\s[на\s]?]?послезавтра.*'
    samp = re.search(sample, s)
    if samp:
        good = True
        sam = samp.group(0)
        sam = sam.split(' ')
        if 'на' in sam:
            sam.remove('на')
        if 'послезавтра' in sam:
            sam.remove('послезавтра')
    if good:
        s = " ".join(sam)
    
    print ("Date: ", date)
    print (s)
    #TODO: код чтобы находить даты заканчивается здесь

    if (s.find("прогноз")>=0):
        if (s.find("погода") >= 0 or s.find("погоду") >= 0 or s.find("погоде") >= 0 or s.find("погоды") >= 0):
            s = s.replace("прогноз", "")
        else:
            s = s.replace("прогноз", "погода")

    m = re.search('.*погода?у?е?ы?.*', s)

    if m:
        bo = False
        service = "weather"
        m = re.search('погода?у?е?ы?\s?в?\s?\w+.*', s)
    if m:
        mystr = m.group(0)
        mystr = mystr.split(" ")
        if len(mystr) > 1:
            print(mystr)
            res1 = ""
            start = 1234 # max value number
            if "в" in mystr:
                start = mystr.index("в")

            if "погода" in mystr:
                start = mystr.index("погода")
                if "в" in mystr:
                    start = mystr.index("в")

            if start+3<=len(mystr): 
                for x in range(start+1, start+3):       
                    res1 = res1 + mystr[x] + " "
            elif start+1<len(mystr): res1 = mystr[start+1]
            bo = True
            city = res1

            print(city)

    m = re.search('\w+\sпогода?у?е?ы?\s?в?\s?', s)

    if m and bo == False:
        mystr = m.group(0)
        mystr = mystr.split(" ")
        res2 = mystr[0]
        city =  res2

        if city=="": city="Алматы"

    
    #end weather service check
    if service=="weather":
       return [service, city, date]
    
    # check for currency services
    
    currencyList = {
	"юань": "CNY",
	"доллар": "USD",
	"дирхам": "AED",
	"песо": "ARS",
	"динар": "KWD",
	"биткоин": "BTC",
	"рубль": "RUB",
	"евро": "EUR",
	"фунт": "GBP",
	"сом": "KGS",
	"тенге": "KZT"
    }
    plainText = uinput
    plainText = plainText.lower()
    plainText = plainText.split(' ')
    plainTextLength = len(plainText)
    preLength = 0
    curr = 1
    realWord = ""
    ind = 0
    finalFirstCurr = ""
    finalSecondCurr = ""
    service=""
    
    if plainText:
        for i in range(0, plainTextLength):
            firstCurr = plainText[i]
            if (firstCurr == "в"):
                ind = i + 1
                break
            for key, value in currencyList.items():
                for j in range(1, min(len(firstCurr), len(key))):
                    if (firstCurr[:j] == key[:j]):
                        if (j > preLength):
                            preLength = j
                            finalFirstCurr = value
                            realWord = firstCurr
        preLength = 0
        for i in range(ind, plainTextLength):
            secondCurr = plainText[i]
            for key, value in currencyList.items():
                for j in range(1, min(len(secondCurr), len(key))):
                    if (secondCurr[:j] == key[:j]):
                        if (j > preLength):
                            preLength = j
                            finalSecondCurr = value
        for i in range(0, plainTextLength):
            if (plainText[i] == realWord):
                if (i - 1 >= 0):
                    try:
                        curr = int(plainText[i - 1])
                    except ValueError:
                        print("Not a number")

    if (finalFirstCurr!="" and finalSecondCurr!=""): 
	    for key, value in currencyList.items():
		    if (realWord[:4] == key[:4]):
			    service="currency"
    print(service, finalFirstCurr, finalSecondCurr, curr)
    if service=="currency":
       print(service)
       return [service, finalFirstCurr, finalSecondCurr, curr]
    # end check for currency services

    #check for youtube service keywords
    plainTextStr = us
    plainTextStr = plainTextStr.lower()
    plainText = plainTextStr.split(' ')
    plainTextLength = len(plainText)

    forSearch = 'смотреть посмотреть поставь клип видео youtube ютуб'
    forSearch = forSearch.split(' ')
    result = ''
    service = ''
    
    
    if plainText:
        for i in range(0, plainTextLength):
            have = 0
            for j in range(0, len(forSearch)):
                if (plainText[i] == forSearch[j]):
                    have = 1
                    service = 'youtube'
            if (plainText[i] == 'на' and (plainText[i + 1] == 'youtube' or plainText[i + 1] == 'ютуб')):
                continue
            if not (have):
                result += plainText[i]
                result += ' '
    #end youtube service check
    if service=="youtube":
        
        return [service, result]
  
    # check for translate service
    plainText = us
    plainText = plainText.lower()
    plainText = plainText.split(' ')
    plainTextLength = len(plainText)
    service = ""

    forSearch = 'слово слова на как'
    forSearch2 = 'перевод переведи переводится перевести'
    forSearch3 = 'перевести с ... на ... слово'
    forSearch = forSearch.split(' ')
    forSearch2 = forSearch2.split(' ')
    forSearch3 = forSearch3.split(' ')

    finalLangToTranslate = "ru"
    textToTranslate = ""
    firstIndex = 0 
    secondIndex = 0 
    thirdIndex = 0
    preLength = 0
    realWord = ""
    
    if plainText:
        for i in range(0, plainTextLength):
            langToTranslate = plainText[i]
            for key, value in langList.items():
                for j in range(1, min(len(langToTranslate), len(key))):
                    if (langToTranslate[:j] == key[:j]):
                        if (j > preLength):
                            preLength = j
                            finalLangToTranslate = value
                            realWord = langToTranslate	

        for k in range(0, len(forSearch)):
            if (forSearch[k] == realWord):
                realWord = ""				
        for k in range(0, len(forSearch2)):
            if (forSearch2[k] == realWord):
                realWord = ""

        for i in range(0, plainTextLength):
            if (plainText[i] == realWord):
                plainText[i] = ""
                continue
            if (plainText[i] == forSearch[0] or plainText[i] == forSearch[1]):
                firstIndex = i + 1
            if (plainText[i] == forSearch[2]):
                secondIndex = i	
            for j in range(0, len(forSearch2)):
                if (plainText[i] == forSearch2[j]):
                    thirdIndex = i + 1
                    if (plainText[i - 1] == forSearch[3]):
                        plainText[i - 1] = ""
        if (firstIndex and secondIndex):
            if (firstIndex < secondIndex):
                for i in range(firstIndex, secondIndex):
                    if (plainText[i] != ""):
                        textToTranslate += plainText[i]
                        textToTranslate += " "
            if (firstIndex > secondIndex):
                for i in range(firstIndex, plainTextLength):
                    if (plainText[i] != ""):
                        textToTranslate += plainText[i]
                        textToTranslate += " "
	
        elif (thirdIndex):
            if not (secondIndex):
                finalLangToTranslate = "ru"
                if (thirdIndex - 2 >= 0 and plainText[thirdIndex - 2] != ""):
                    for i in range(0, thirdIndex - 1):
                        if (plainText[i] != ""):
                            textToTranslate += plainText[i]
                            textToTranslate += " "
                else:
                    for i in range(thirdIndex, plainTextLength):
                        if (plainText[i] != ""):
                            textToTranslate += plainText[i]
                            textToTranslate += " "			
            else:
                if (thirdIndex < secondIndex):
                    for i in range(thirdIndex, secondIndex):
                        if (plainText[i] != ""):
                            textToTranslate += plainText[i]
                            textToTranslate += " "
                elif (thirdIndex - 2 >= 0 and plainText[thirdIndex - 2] != ""):
                    for i in range(0, thirdIndex - 1):
                        if (plainText[i] != ""):
                            textToTranslate += plainText[i]
                            textToTranslate += " "		
                else:
                    for i in range(secondIndex + 1, plainTextLength):
                        if (plainText[i] != ""):
                            textToTranslate += plainText[i]
                            textToTranslate += " "			
        else:
            for i in range(0, secondIndex):
                if (plainText[i] != ""):
                    textToTranslate += plainText[i]
                    textToTranslate += " "

        
        print("Text: " + textToTranslate + "\nLanguage: " + finalLangToTranslate)
        if (textToTranslate!=""): service = "translate"
    # end translate service check 
    if service=="translate":
        return [service, textToTranslate, finalLangToTranslate]
    # check for wiki services
    
    plaintText = us
    plaintText = plaintText.lower()
    service=''
    forSearch = 'значение определение это'
    forSearch = forSearch.split(' ')
    regEx = '.*значение.*'
    query = ''
    
    words = re.search(regEx, plaintText)
    if (not words):
        regEx = '.*определение.*'
        words = re.search(regEx, plaintText)
    if (not words):
        regEx = '.*это.*'
        words = re.search(regEx, plaintText)
    
    if words:
        words = words.group(0)
        words = words.split(' ')
        wordsLength = len(words)
        
        if (words[wordsLength - 1] == forSearch[0] or words[wordsLength - 1] == forSearch[1] or words[wordsLength - 1] == forSearch[2]):
                for i in range (0, wordsLength - 1):
                    query += words[i]
                    query += ' '
        else:
            for i in range(0, wordsLength):
                if (words[i] == forSearch[0] or words[i] == forSearch[1]):
                    for j in range(i + 1, wordsLength):
                        query += words[j]
                        query += ' '
                        break;	
        if query!='':
            service = 'wiki'
          
            return [service, query]
    
    ## There is end of finding word 'значение'

    forSearch = 'что такое означает'
    forSearch = forSearch.split(' ')
    regEx = '.*что.*'
    query = ''	
    
    words = re.search(regEx, plaintText)
    if (not words):
        regEx = '.*означает.*'
        words = re.search(regEx, plaintText)
    
    if words:
        words = words.group(0)
        words = words.split(' ')
        wordsLength = len(words)
    
        if (wordsLength>2 and words[0] == forSearch[0]):
            forStart = 1
            if (words[1] == forSearch[1] or words[1] == forSearch[2]):
                forStart = 2
                for i in range(forStart, wordsLength):
                    query += words[i]
                    query += ' '
        if (wordsLength>2):
            for i in words:
                if (i == forSearch[0] or i == forSearch[2]):
                    break
                query += i
                query += ' '			
        if query!='':
            service = 'wiki'
            
            return [service, query]

## There is end of finding word 'что такое означает'
    
    forSearch = 'расскажи о про пожалуйста'
    forSearch = forSearch.split(' ')
    regEx = '.*расскажи.*'
    query = ''
    words = re.search(regEx, plaintText)	
    
    
    if words:
        words = words.group(0)
        words = words.split(' ')
        wordsLength = len(words)

    	
        for i in range(0, wordsLength):
            if (wordsLength > 2 and words[i] == forSearch[0]):
                forStart = i + 1
                if (words[i + 1] == forSearch[1] or words[i + 1] == forSearch[2] or words[i + 1] == forSearch[3]):
                    if (words[i + 2] == forSearch[1] or words[i + 2] == forSearch[2]):
                        forStart = i + 3
                    else:	
                        forStart = i + 2	
                for j in range(forStart, wordsLength):
                    query += words[j]
                    query += ' '	
                break
        if query!='':
            service = 'wiki'
            
            return [service, query]
    #end wiki service check
    if service=="wiki":
        
        return [service, query]
    #check for timezone services
    plainText = us
    plainText = plainText.lower()
    plainText = plainText.split(' ')
    plainTextLength = len(plainText)
    
    forSearch = 'время час город городе'
    forSearch = forSearch.split(' ')
    result = ''
    service = ''
    haveV = 0
    city = ''

    
    if plainText:
        for i in range(0, plainTextLength):
            if (plainText[i] == forSearch[2] or plainText[i] == forSearch[3]):
                plainText[i] = ""
            if (plainText[i] == 'в'):
                haveV = 1	
    
    if (plainText):
        for i in range(0, plainTextLength):
            if (plainText[i] == ""):
                continue
            if (haveV == 1 and plainText[i] == 'в' and len(plainText)>i+1):
                if (plainText[i + 1] == "" and len(plainText)>i+2):
                    city = plainText[i + 2]
                else:
                    city = plainText[i + 1]
                break
            if (plainText[i] == forSearch[0] or plainText[i] == forSearch[1] and len(plainText)>i+1):
                service = "time"
                if (haveV != 1):
                    if (i == 0 and len(plainText)>i+1):
                        if (plainText[i + 1] == ""  and len(plainText)>i+2):
                            city = plainText[i + 2]
                        else:
                            city = plainText[i + 1]
                    else:
                        city = plainText[i - 1]

    #end timezone service check

    if service=="time":
        
        return [service, city]

    
    #if no service was found go to chitchat
    
    if service=="":
        service="chitchat"
        return service

