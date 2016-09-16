
from tmspider.items import TmmItem
from tmspider.items import ModelBrief
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
import scrapy
import re
import json

class TmmSpider(BaseSpider):
    name = "TmmSpider"
    allowed_domains = []
    start_urls = ["https://mm.taobao.com/json/request_top_list.htm?page=10"]
    
    detailUrl = "https://mm.taobao.com/self/info/model_info_show.htm?user_id="
    
    def parse(self, response):
        sel = Selector(response)
        for isel in sel.css('.list-item'):
            topSel = isel.css(".top")
            brief = ModelBrief()
            brief.uid= topSel.css(".friend-follow").xpath("./@data-userid").extract_first()
            brief.age = topSel.xpath('./em/strong/text()').extract_first()
            brief.name = topSel.xpath("./a/text()").extract_first()
            brief.photoUrl = "https:" + isel.css(".w610").xpath("./a/@href").extract_first()
            
            detailReq = scrapy.Request(self.detailUrl + brief.uid, callback = self.parseDetail)
            detailReq.meta["Brief"] = brief
            yield detailReq

            photoReq = scrapy.Request(brief.photoUrl, callback = self.parsePhotoImage)
            photoReq.meta["Brief"] = brief
            yield photoReq
            
    def parseDetail(self, response):
        brief = response.meta["Brief"]
        item = TmmItem()
        item["uid"] = brief.uid
        item["name"] = brief.name
        info = response.selector.css(".mm-p-base-info ul")
        item["city"] = info.css("li:nth-child(3) span::text").extract_first().strip()
        item["birthDate"] = self.parseBirthDate(int(brief.age),
                                                info.css("li:nth-child(2) span::text").extract_first().strip())
        item["height"] = self.parseMeter(info.css(".mm-p-height p::text").extract_first().strip(), "CM")
        item["weight"] = self.parseMeter(info.css(".mm-p-weight p::text").extract_first().strip(), "KG")
        msize = info.css(".mm-p-size p::text").extract_first().strip().split("-")
        item["waist"] = float(msize[0])
        item["bust"] = float(msize[1])
        item["hip"] = float(msize[2])
        item["cup"] = self.parseCup(info.css(".mm-p-bar p::text").extract_first().strip())

        yield item


    def parsePhotoImage(self, response):
        s = response.selector.xpath('//input[@id="J_MmPicListId"]/@value').extract_first()
        images = json.loads(s)
        for i in range(1, 4):
            image = images[i]
            print(image["bigUrl"])
    
    def parseCup(self, s):
        c = s.upper()[-1]
        if c.isalpha():
            return c
        return None

    def parseMeter(self, s, unit):
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

