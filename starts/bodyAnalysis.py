# -*- coding: utf-8 -*-

import re
from enum import Enum
    
class Body(object):
    __slots__ = ("name", "birthDate", "height", "weight",
                 "bust", "waist", "hip", "cup", "memo")
    def __init__(self):
        self.name = ""
        self.birthDate = ""
        self.height = 0.0
        self.weight = 0.0
        self.bust = 0.0
        self.waist = 0.0
        self.hip = 0.0
        self.cup = ""
        self.memo = ""
       
    def __str__(self):
        return "%s,(%s),%.1f,%.1f,(%.1f %s,%.1f,%.1f),%s"\
            %(self.name, self.birthDate, self.height, self.weight, self.bust, self.cup, self.waist, self.hip, self.memo)

#Item = Enum("Item", ("Name", "BirthDate", "Height", "Weight", "ThreeDim","Other"))

class Tokenizer(object):
    End = '\x00'
    def __init__(self,s):
        words = re.split("[-\(\),\n：、（）/:，]|　+| +||\W+", s)
        self.it = iter([w for w in words if w])
        self.__cur = None
        self.__ns = None
        self.__regex = re.compile("(\d+(\.(\d)?)?)(.*)")

    def next(self):
        self.__cur = self.__next()
        print("Token: " + self.__cur)
        return self.__cur

    def ignoreMaybe(self, words):
        if self.__cur.upper() in words:
            self.next()

    @property
    def cur(self):
        if not self.__cur:
            raise ValueError("no cur value, call next() first")
        return self.__cur

    @property
    def isEnd(self):
        return self.__cur != Tokenizer.End
    
    def __next(self):
        if self.__ns:
            s = self.__ns
            self.__ns = None
            return s
        else:
            try:
                ns = next(self.it)
                m = self.__regex.match(ns)
                if m:
                    s = m.group(1)
                    self.__ns = m.group(4) #maybe empty
                else:
                    s = ns
                    self.__ns = None
                return s
            except StopIteration:
                return Tokenizer.End


def parseBirthDate(tag, tk, isTag, body):
    m1 = re.match("(\d+)((\.(\d+))(\.(\d+))?)?", tk.cur)
    if not m1:
        m1 = re.match("(\d+)年(((\d+)月)((\d+)日)?)?", tk.cur)
    if m1:
        body.birthDate =  m1.group(1)
        if m1.group(4):
            body.birthDate = body.birthDate + "-" + m1.group(4)
        if m1.group(6):
            body.birthDate = body.birthDate + "-" + m1.group(6)
        tk.next()            
    else:
        raise ValueError("Birthdate got (%s)"%(tk.cur))
    
def parseHeight(tag, tk, isTag, body):
    s = tk.cur
    ht = 0.0
    if s.isdigit():
        ht = float(s)
        u = tk.next().upper()
        if u == "CM" or u == "厘米" or u == "公分":
            tk.next()
        elif u == "M" or u == "米" :
            ht = ht * 100.0
            tk.next()
        body.height = ht
    else:
        raise ValueError("Height got (%s)"%(s))
    
def parseWeight(tag, tk, isTag, body):
    s = tk.cur
    wt = 0.0
    if s.isdigit():
        wt = float(s)
        u = tk.next().upper()
        if u == "LB" or u == "LBS" or u == "磅":
            tk.next()
            wt = wt / 2.2
        elif u == "KG" or u == "千克" or u == "公斤":
            tk.next()
        elif u == "斤":
            wt = wt / 2.0
            tk.next
        else:
            pass # nothing to do
        body.weight = wt
    else:
        raise ValueError("Weight got (%s)"%(s))

def parseBwh(tag, tk, isTag, body):
    units = ["英寸", "INCH", "厘米", "CM", "公分", '"']
    cup = cupMaybe(tk)
    tk.ignoreMaybe(["B", "胸围"])
    if not tk.cur.isdigit():
        raise ValueError("bust got (%s)"%(tk.cur))
    body.bust = inch2cmMaybe(float(tk.cur))
    tk.next()
    if not cup:
        cup = cupMaybe(tk)
    body.cup = cup
    tk.ignoreMaybe(units)
    print("after bust")

    tk.ignoreMaybe(["W", "腰围"])
    if not tk.cur.isdigit():
        raise ValueError("Waist got (%s)"%(tk.cur))
    body.waist = inch2cmMaybe(float(tk.cur))
    tk.next()
    tk.ignoreMaybe(units)
    print("after waist")
    
    tk.ignoreMaybe(["H", "臀围"])
    if not tk.cur.isdigit():
        raise ValueError("hip got (%s)"%(tk.cur))
    body.hip = inch2cmMaybe(float(tk.cur))
    tk.next()
    tk.ignoreMaybe(units)
    print("after hip: " + tk.cur)

def parseMemo(tag, tk, isTag, body):
    body.memo = tag + " " + tk.cur + ", " + body.memo
    tk.next
    
def inch2cmMaybe(x):
    if x < 40:
        return x * 2.54
    return x

def cupMaybe(tk):
    c = tk.cur.upper()
    if c in {"A", "B", "C", "D", "E", "F"}:
        tk.next()
        return c
    else:
        return ""
            
class DataParser(object):
    def __init__(self):
        self.parserMap={}
        self.parserMap["出生日期"] = parseBirthDate
        self.parserMap["出生年月"] = parseBirthDate
        self.parserMap["生日"] = parseBirthDate
        
        self.parserMap["身高"] = parseHeight
        self.parserMap["体重"] = parseWeight
        self.parserMap["三围"] = parseBwh
        
        self.parserMap["血型"] = parseMemo
        self.parserMap["星座"] = parseMemo
        self.parserMap["生肖"] = parseMemo
        self.parserMap["出生地"] = parseMemo
        self.parserMap["英文名"] = parseMemo
        self.parserMap["籍贯"] = parseMemo
        self.parserMap["原名"] = parseMemo
        self.parserMap["本名"] = parseMemo
    
        self.isTag = lambda t : self.parserMap.get(t)

    def process(self, tk):
        records = []
        while tk.cur.isdigit(): #Record Number
            print("process record " + tk.cur)
            t = tk.next() # pass by the record number
            b = self.processRec(tk)
            if b:
                records.append(b)
        return records

    def processRec(self, tk):
        b = Body()
        b.name = tk.cur
        tk.next()
        print(tk.cur)
        p = self.parserMap.get(tk.cur)
        while p:
            tag = tk.cur
            tk.next()
            p(tk.cur, tk, self.isTag, b)
            p = self.parserMap.get(tk.cur)
        return b

def parseFile():
    with open("d:/home/sources/py/body-data0.txt", "r") as f:
        s = f.read()
        doit(s)
        
def doit(s):
    tk = Tokenizer(s)
    p = DataParser()
    tk.next()
    rx = p.process(tk)
    print("Got %d records"%(len(rx)))
    i=1
    for r in rx:
        print(i)
        print(r)
        i = i + 1
    
s1="""1,钟丽缇  
　　出生日期：1970.6.19 
　　身高：168cm  
　　体重：108lbs 
　　三围：36、 24、 35（英寸）
   12，林志玲
   身高:174cm 体重:52 kg 三围:34E、24、36（英寸）"""
