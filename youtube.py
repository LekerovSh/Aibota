import requests

def youtube_search(text_search):
    YOUTUBE_KEY = "AIzaSyCxA8iUtg22vs6nmE0aDh8ek5p9UVz9f9k"
    try:
        res = requests.get("https://www.googleapis.com/youtube/v3/search",
                           params={"part": "id", "q": text_search, "type": "video", "key": YOUTUBE_KEY})
        data = res.json()
        print(data)
        data = data['items'][0]['id']['videoId']
        data = "https://www.youtube.com/watch?v=" + data
    except:
        data = "Сервер временно не отвечает. Пожалуйста, попробуйте попытку позже."
    return "Показан результат по запросу <a href='"+data+"'>"+text_search+"</a>"
