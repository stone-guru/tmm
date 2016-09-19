# -*- coding: utf-8 -*-
from tmspider.db.pgdao import PgDao
from pathlib import Path
from scrapy.exceptions import DropItem


class TmmSpiderPipeline(object):
    imageDir = Path("/home/bison/Pictures/tmm")
    stageDir = None
    stage = 1  # tmp value
    dao = None

    def __init__(self):
        self.dao = PgDao()
        self.stage = self.dao.stage
        self.stageDir = self.imageDir.joinpath("stage" + str(self.stage))
        self.stageDir.mkdir(0o755)

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
        suffix = suffixOfImage(imageBytes)
        fn = "{}-{}-{}{}".format(item["uid"], item["name"], item["index"], suffix)
        fp = self.stageDir.joinpath(fn)
        with fp.open("wb") as f:
            f.write(imageBytes)
        # return item
        pass


def suffixOfImage(data):
    if data.startswith(b'\377\330'):
        return ".jpg"
    if data.startswith(b'\211PNG\r\n\032\n'):
        return ".png"
    if data[:6] in (b'GIF87a', b'GIF89a'):
        return ".gif"
    if data[:2] in (b'MM', b'II'):
        return '.tiff'
    if len(data) >= 3 and data[0] == ord(b'P') \
       and data[1] in b'14' and data[2] in b' \t\n\r':
        return '.pbm'
    if data.startswith(b'BM'):
        return '.bmp'
    return ".jpg"
