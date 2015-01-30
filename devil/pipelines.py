# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import sys
import re
import os

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

def opencc(txt):
    out = os.popen("echo '{0}' | opencc".format(txt))
    return out.read().strip()

class DevilPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool("MySQLdb",
                                            host="localhost",
                                            db="ch4_comics",
                                            user="root",
                                            passwd="123",
                                            cursorclass=MySQLdb.cursors.DictCursor,
                                            charset="utf8",
                                            use_unicode=True
        )

    def process_item(self, item, spider):
        print spider.name
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)
        return item

    def do_insert(self, db, item):
        ccid = self.check_exist(db, item)
        print ccid
        print "howhow"
        if ccid is None:
            sql = "INSERT `ch4_comic`(`title`,`year`,`area`,`desc`,`isclosed`,`eps`,`hits`, `type`, `director`, `actors`, `pic`) \
                VALUES('%s', '%s', '%s', '%s', 0, '%s', '%s', '%s', 'DIR', 'ACTS', '%s');" %  \
                (opencc(item['title']), item['year'], opencc(item['area']), opencc(item['desc'].strip()),
                 item['eps'], item['hits'], opencc("|".join(item['type'])), item['pic'])
            print sql
            db.execute(sql)
            db.execute("SELECT LAST_INSERT_ID() AS ccid")
            ccid = db.fetchone()['ccid']
        else:
            ccid = ccid['ccid']
            sql = "UPDATE `ch4_comic` SET `eps` = {0}, `hits` = {2}, `pic` = '{3}' WHERE `ccid` = {1}".format(item['eps'], ccid, item['hits'], item['pic'])
            print "Update #{0}#".format(sql)
            db.execute(sql)

        print "ccid: ", ccid
        for ep in item['ep_list']:
            ccsid = self.check_ep(db, ep['src_type'], ep['key'])
            if ccsid is None:
                sql = "INSERT `ch4_comic_srcs`(`type`,`org_url`,`key`,`ccid`,`ep`, `ep_title`) VALUES({0:d}, '{1}','{2}','{3:d}', '{4:d}', '{5}');".format(ep['src_type'], ep['org_url'], ep['key'], ccid, ep['ep'], opencc(ep['ep_title']))
                db.execute(sql)
            else:
                print "Exist!"
            # print sql

    def check_exist(self, db, item):
        print "check"
        db.execute("SELECT `ccid` FROM ch4_comic WHERE `title` = '%s'" % item['title'])
        return db.fetchone()

    def check_ep(self, db, type, key):
        db.execute("SELECT `ccsid` FROM `ch4_comic_srcs` WHERE `key` = '{0}' AND `type` = {1};".format(key, type))
        return db.fetchone()

    def handle_error(self, e):
        sys.stderr.write(str(e))
