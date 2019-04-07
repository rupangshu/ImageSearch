from bs4 import BeautifulSoup
import json
import urllib.request as urllib2
import urllib.parse
import urllib.error
from MongoDBUtil import MongoPersist
import base64


class SearchImageWrap:
    def get_soup(self, url, header):
        request = urllib.request.Request(url, headers=header)
        return BeautifulSoup(urllib.request.urlopen(request), 'html.parser')

    def searchImg(self, keyword):
        query = keyword
        image_type = "Action"
        url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
        print(url)
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        soup = self.get_soup(url, header)

        ActualImages = []  # contains the link for Large original images
        for a in soup.find_all("div", {"class": "rg_meta"}):
            link, Type = json.loads(a.text)["ou"], json.loads(a.text)["ity"]
            ActualImages.append((link, Type))

        print("there are total", len(ActualImages), "images")

        keywordjsonarray = []
        keywordjson = {}
        keywordjson["keyword"] = keyword
        keywordjson["images"] = []
        for i, (img, Type) in enumerate(ActualImages[0:5]):
            try:
                req = urllib2.Request(img, headers=header)
                raw_img = urllib2.urlopen(req).read()

                if len(Type) == 0:
                    imagename = image_type + "_" + str(i) + ".jpg"
                else:
                    imagename = image_type + "_" + str(i) + "." + Type
                imgContent = base64.b64encode(raw_img)
                imagedata = {}
                imagedata["content"] = imgContent
                imagedata["name"] = imagename
                keywordjson["images"].append(imagedata)
                print("found images from web - "+imagename);
            except Exception as e:
                print("could not load : " + img)
                print(e)
        keywordjsonarray.append(keywordjson)
        try:
            MongoPersist().insertIntoMongodb(keywordjsonarray)
        except Exception as e:
            print("Exeception occured while performing database operation")
            print(e)

    def getdetails(self, keyword):

        try:
            result = MongoPersist().searchMongodb(keyword)
        except Exception as e:
            print("Exeception occured while performing database operation")
            print(e)
        outputList = []
        for data in result["images"]:

            for key, value in data.items():
                if key == "content":
                    data[key] = value.decode()
            outputList.append(data)

        return outputList
