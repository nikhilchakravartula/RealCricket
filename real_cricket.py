from sms_notifier import TwilioNotify
import requests
from bs4 import BeautifulSoup as BS
import global_variables as gv
import summary_feed
import desktop_notifier as dn
from threading import *
import time


def worker_thread():
    summary_feed.load_from_rss()
    message = ""
    print(type(gv.matches))
    print(gv.matches)
    for match_id in gv.matches.keys():
        message+= gv.matches[match_id].summary()+"\n"
    dn.balloon_tip("Real Cricket", message)


def main():
    live_matches_urls = []
    live_matches_titles = []

    try:
        page = requests.get(gv.LIVE_MATCHES_URL)
        if page.status_code!=200:
            raise ValueError("Could not connect to the webpage")
        soup = BS(page.content, 'html.parser')

        for anchor in soup.find_all('a', {'class': 'cb-mat-mnu-itm cb-ovr-flo'}):
            title = anchor['title']
            if title.split(" ")[-1:][0].lower() in gv.LIVE_IDENTIFIERS:
                live_matches_urls.append(anchor['href'])
                live_matches_titles.append(anchor['title'])

        for current_match in live_matches_urls:
            page = requests.get(gv.ROOT_URL+current_match)
            soup = BS(page.content, 'html.parser')
            print(soup.prettify())
    except ValueError as value_error:
        print(value_error.args)

    finally:
        print()

if __name__ == '__main__':
    time_interval = 60
    summary = ""
    while 1:
        thread = Thread(target=worker_thread)
        thread.start()
        thread.join()
        time.sleep(time_interval)

