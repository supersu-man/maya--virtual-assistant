import webbrowser
import requests
import oxford


def googleSearch(query):
    url = f"https://www.google.com/search?q=" + query
    headers = {
        "referer": "referer: https://www.google.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
    }
    response = requests.get(url, headers=headers).text
    results = response.split("Web result")[1].split("href=\"")
    link1 = results[1].split("\"")[0]
    if link1.count("/") == 3:
        temp = link1.split("/")
        link1 = link1.replace(temp[-1], "")
    return link1


def openWebsite(site):
    webbrowser.open(site)


def whatIs(word):
    oxford.Word.get(word)
    v = oxford.Word.definitions()
    return v[0]
