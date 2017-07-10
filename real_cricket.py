from sms_notifier import TwilioNotify
import requests
from bs4 import BeautifulSoup as BS
import global_variables as gv
import summary_feed
import desktop_notifier as dn
from threading import *
import time
import re
from enum import Enum

class TYPE_OF_FEED(Enum):
    SUMMARY = 0
    BALL = 1

class over_summary:
    def __init__(self,desc,over,color):
        self.desc=desc
        self.over=over
        self.color=color

def worker_thread(flag):
    message = ""
    if flag == TYPE_OF_FEED.SUMMARY:
        summary_feed.load_from_rss()
        print(type(gv.matches))
        print(gv.matches)
        for match_id in gv.matches.keys():
            message+= gv.matches[match_id].summary()+"\n"
    elif flag == TYPE_OF_FEED.BALL:
        print("Started scrape")
        summary_feed.scrape()
        print("After scrape", gv.current_stats_str)

        message = gv.current_stats_str
    dn.balloon_tip("Real Cricket", message)


def main():
    print()

if __name__ == '__main__':
    time_interval = 20
    summary = ""

    while 1:
        thread = Thread(target=worker_thread,args=(TYPE_OF_FEED.BALL,))
        thread.start()
        thread.join()
        time.sleep(time_interval)
