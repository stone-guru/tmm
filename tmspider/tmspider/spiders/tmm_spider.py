
from tmspider.items import TmmItem
from tmspider.items import ImageItem
from tmspider.items import ModelBrief
from scrapy.spiders import Spider
from scrapy.selector import Selector
# from scrapy.settings import Settings
import scrapy
import re
import json


class TmmSpider(Spider):
    name = "TmmSpider"
    allowed_domains = []
    start_urls = []

    iStart = 1
    iEnd = 1
    iPage = 1
    modelListUrl = "https://mm.taobao.com/json/request_top_list.htm?page="
    detailUrl = "https://mm.taobao.com/self/info/model_info_show.htm?user_id="
    nImagePerModel = 2

    def __init__(self, start, end):
        super(TmmSpider, self).__init__()

        self.iStart = int(start)
        self.iEnd = int(end)
        self.iPage = self.iStart
        self.start_urls = [self.modelListUrl + str(self.iStart)]
        print("Fetch mm from page {} to page {}".format(self.iStart, self.iEnd))
        
    def parse(self, response):
        sel = Selector(response)
        for isel in sel.css('.list-item'):
            topSel = isel.css(".top")
            brief = ModelBrief()
            brief.uid = topSel.css(".friend-follow").xpath("./@data-userid").extract_first()
            brief.age = topSel.xpath('./em/strong/text()').extract_first()
            brief.name = topSel.xpath("./a/text()").extract_first()
            brief.photoUrl = "https:" + isel.css(".w610").xpath("./a/@href").extract_first()

            detailReq = scrapy.Request(self.detailUrl + brief.uid, callback=self.parseDetail)
            detailReq.meta["Brief"] = brief
            yield detailReq

            photoPageReq = scrapy.Request(brief.photoUrl, callback=self.parsePhotoPage)
            photoPageReq.meta["Brief"] = brief
            yield photoPageReq

        self.iPage += 1
        if self.iPage <= self.iEnd:
            yield scrapy.Request(self.modelListUrl + str(self.iPage), callback=self.parse)

    def parseDetail(self, response):
        brief = response.meta["Brief"]
        item = TmmItem()
        item["itemType"] = "modelInfo"
        item["uid"] = brief.uid
        item["name"] = brief.name
        info = response.selector.css(".mm-p-base-info ul")
        item["city"] = info.css("li:nth-child(3) span::text").extract_first().strip()
        item["birthDate"] = self.parseBirthDate(int(brief.age),
                                                info.css("li:nth-child(2) span::text").extract_first())
        item["height"] = self.parseMeter(info.css(".mm-p-height p::text").extract_first(), "CM")
        item["weight"] = self.parseMeter(info.css(".mm-p-weight p::text").extract_first(), "KG")
        msize = info.css(".mm-p-size p::text").extract_first().strip().split("-")
        item["waist"] = float(msize[0])
        item["bust"] = float(msize[1])
        item["hip"] = float(msize[2])
        item["cup"] = self.parseCup(info.css(".mm-p-bar p::text").extract_first().strip())

        yield item

    def parsePhotoPage(self, response):
        s = response.selector.xpath('//input[@id="J_MmPicListId"]/@value').extract_first()
        images = json.loads(s)
        i = 0
        while (i < self.nImagePerModel and i < len(images)):
            image = images[i]
            imageReq = scrapy.Request("https:" + image["bigUrl"], self.fetchImage)
            imageReq.meta["Brief"] = response.meta["Brief"]
            imageReq.meta["index"] = i + 1
            i += 1
            yield imageReq

    def fetchImage(self, response):
        brief = response.meta["Brief"]
        imageBytes = response.body
        print("Got image for {} {}, image size is {}.".format(brief.uid, brief.name, len(imageBytes)))
        item = ImageItem()
        item["itemType"] = "modelImage"
        item["uid"] = brief.uid
        item["name"] = brief.name
        item["imageBytes"] = imageBytes
        item["index"] = response.meta["index"]
        yield item

    def parseCup(self, s):
        c = s.upper()[-1]
        if c.isalpha():
            return c
        return None

    def parseMeter(self, t, unit):
        s = t.strip()
        if s.upper().endswith(unit):
            return float(s[:-len(unit)])
        return float(s)

    def parseBirthDate(self, age, s):
        y = 2016 - age + 1
        m1 = re.search("(\d+)\W*月\W*(\d+)日", s)
        if not m1:
            return str(y)
        else:
            return "{}-{}-{}".format(y, int(m1.group(1)), int(m1.group(2)))
