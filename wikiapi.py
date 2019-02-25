# надо установить библиотеку => pip install wikipedia
import wikipedia
from bs4 import BeautifulSoup

# наш метод
#######################################################################################

def wikiapp(word):
    desc = ""
    page = wikipedia.wikipedia.WikipediaPage
    wikipedia.set_lang("ru")
    try:
        page = wikipedia.page(word)
        print(page.url)
    except wikipedia.exceptions.PageError as pageError:
        desc = "По вашему запросу ничего не найдено."
    except wikipedia.exceptions.DisambiguationError as e:
        desc = "По вашему запросу было найдено несколько ответов. Уточните свой запрос."
        #page = wikipedia.page(str(e.options[1]))
        #print("options " + e.options[1])
        #print(type(page))
        #print("Найденные страницы:\n" + str(e.options))
    finally:
        if (page != wikipedia.wikipedia.WikipediaPage):
            desc = page.summary
    #print(type(page))
    #print("_____________________________________________________________")
    return desc


#######################################################################################


#print(wikiapp(input()))
