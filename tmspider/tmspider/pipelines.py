# -*- coding: utf-8 -*-
from tmspider.db.pgdao import PgDao

import re
from pathlib import Path 

from scrapy.exceptions import DropItem

class TmmSpiderPipeline(object):
    imageDir = Path("/home/bison/Pictures/tmm")
    dao = None
    
    def __init__(self):
        self.dao = PgDao()
        
    def process_item(self, item, spider):
        if item["itemType"] == "modelInfo":
            return self.processModelInfo(item)
        elif item["itemType"] == "modelImage":
            return self.processModelImage(item)
        else:
            raise DropItem("unknown type Item")

    def processModelInfo(self, item):
        self.dao.saveModelItem(item)
        return item

    def processModelImage(self, item):
        imageBytes = item["imageBytes"]
        item["imageBytes"] = len(imageBytes)
        fn = "{}-{}-{}{}".format(item["uid"], item["name"], item["index"], item["suffix"])
        fp = self.imageDir.joinpath(fn)
        with fp.open("wb") as f:
            f.write(imageBytes)
        # return item
        pass

