# -*- coding: utf-8 -*-

import psycopg2


class PgDao:
    conn = None
    cursor = None
    stage = 1

    def __init__(self):
        self.conn = psycopg2.connect(host="localhost", database="tmm",
                                     user="bison", password="123456")
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        self.stage = self.getAndIncStageNum()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def getAndIncStageNum(self):
        self.cursor.callproc("f_stage_num")
        sn = self.cursor.fetchone()[0]
        return sn

    def saveModelItem(self, item):
        self.cursor.callproc("insert_model",
                             [self.stage, item['uid'], item['name'], item['birthDate'], item['height'],
                              item['weight'], item['waist'], item['bust'], item['hip'], item['cup']])
