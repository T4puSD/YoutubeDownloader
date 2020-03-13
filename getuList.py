from bs4 import BeautifulSoup
import requests


class SongListGenerator:
    def prepareLinks(self, songList):
        youtubeUrl = "www.youtube.com"
        tempList = []
        for i in songList:
            tempList.append(youtubeUrl+i)
        return tempList

    def generateList(self, url):
        page = requests.get(url)

        # Making sets
        uniqueUrls = {1, 2, 3}
        uniqueUrls.clear()
        if(page.status_code == 200):
            soup = BeautifulSoup(page.text, 'html.parser')
            atags = soup.find_all('a')
            for i in atags:
                href = i['href']
                if(href.startswith('/watch?')):
                    if i.text.strip() in ['[Deleted video]','[Private video]']:
                        uniqueUrls.add(href.split('&')[0])
                        # tempUrl = ""
                        # for i in range(0, len(href)):
                        #     if(href[i] != "&"):
                        #         tempUrl += href[i]
                        #     else:
                        #         break
                        # uniqueUrls.add(tempUrl)
        else:
            print("error occured in fetching the page")
        # print(uniqueUrls)
        songList = list(uniqueUrls)
        songList = self.prepareLinks(songList)
        return songList

if __name__ == "__main__":
    bot = SongListGenerator()
    # list1 = bot.generateList("https://www.youtube.com/playlist?list=PLRiSVT9MWtYx6Beo5I_JFBWdisVO-6mI5")
    list1 = bot.generateList("https://www.youtube.com/playlist?list=PLRiSVT9MWtYxEZEGnmGePWt0w7P9IZZ8H")
    print(list1)
    print(len(list1))
