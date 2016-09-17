# -*- coding: utf-8 -*-

import psycopg2

class PgDao:
    conn = None
    cursor = None
    def __init__(self):
        self.conn = psycopg2.connect(host = "localhost", database = "tmm", user = "bison", password = "timeismoney")
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()
    
    def getAndIncStageNum(self):
        self.cursor.execute("select NEXT_STAGE from STAGE_NUM;")
        sn = self.cursor.fetchone()[0]
        self.cursor.execute("update STAGE_NUM set NEXT_STAGE = NEXT_STAGE + 1");
        self.conn.commit()
        return sn

    def saveModelItem(self, item):
        pass
    
