
from tmspider.items import TmmItem
from scrapy.spider import BaseSpider
from scrapy.selector import Selector

class BriefSpider(BaseSpider):
    name = "Brief"
    allowed_domains = []
    start_urls = \
        ["https://mm.taobao.com/json/request_top_list.htm?page=" + str(i) for i in range(1, 8)]

    def parse(self, response):
        sel = Selector(response)
        for isel in sel.css('.list-item'):
            item = TmmItem()
            topSel = isel.css(".top")
            item["uid"] = topSel.css(".friend-follow").xpath("./@data-userid").extract_first()
            item["age"] = topSel.xpath('./em/strong/text()').extract_first()
            item["name"] = topSel.xpath("./a/text()").extract_first()
            item["photoUrl"] = isel.css(".w610").xpath("./a/@href").extract_first()
            yield item
            
        
