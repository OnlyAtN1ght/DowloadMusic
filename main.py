import urllib.request
import bs4 as bs
import ssl
import requests
import os


URL = "http://mp3-skulls.net/"
context = ssl._create_unverified_context()

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

def main():
    #typ = int(input("1 for Song\n2 for Album\n"))
    typ = 2
    #name = str(input("What {}\n".format(typ)))
    name = "The Marshall Mathers LP"
    name = name.replace(" ","+")

    if typ == 1:
        typ = "Song"
        requestUrl = "http://mp3-skulls.net/music/search.php?ty=" + name + "&sh=" + typ
        opener = AppURLopener()
        page = opener.open(requestUrl)
        soup = bs.BeautifulSoup(page,"html.parser")
        element = soup.findAll("a",{"class":"touch"})
        downloadSong(element[0]["href"],findName(element[0]["href"]))

    if typ == 2:
        typ = "Album"
        requestUrl = "http://mp3-skulls.net/music/search.php?ty=" + name + "&sh=" + typ
        opener = AppURLopener()
        page = opener.open(requestUrl)
        soup = bs.BeautifulSoup(page, "html.parser")
        url = soup.findAll("a", {"class": "touch"})[0]["href"]
        opener = AppURLopener()
        page = opener.open(url)
        soup = bs.BeautifulSoup(page,"html.parser")
        if not os.path.exists(name+"/"):
            os.mkdir(name)

        for element in soup.findAll("a",{"class":"lk"}):
            fileName = name +  "/"  + findName(element["href"])  + ".mp3"
            downloadSong(element["href"],fileName)


def downloadSong(url,fileName):
    opener = AppURLopener()
    page = opener.open(url)
    soup = bs.BeautifulSoup(page,"html.parser")
    element = soup.findAll("div",{"class":"dark brd style78"})
    tag = element[len(element)-1].findAll("a")
    html = tag[0].get("href")
    opener = AppURLopener()
    page = opener.open(html)
    r = requests.get(html, stream=True)

    with open(fileName, 'wb') as f:
        for chunk in r.iter_content(512):
            if chunk:
                f.write(chunk)

def findName(name):
    name = str(name)
    name = name[:-5]
    name = name [::-1]
    i=0
    for letter in name:
        i+=1
        if letter == '/':
            name = name[:i-1]
            return name[::-1]

if __name__ == "__main__":
    main()