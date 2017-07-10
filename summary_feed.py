import global_variables as gv
import xml.etree.ElementTree as ET
import requests
import CricketMatch as CM


def load_from_rss():
    gv.matches.clear()
    page = requests.get(gv.RSS_FEED_URL)
    root = ET.fromstring(page.content.decode("utf-8"))
    for match in root.findall('./match'):
        print(match.attrib.get('srs'))
        venue = CM.Venue(match.attrib.get('grnd'), match.attrib.get('vcity'), match.attrib.get('vcountry'))
        match_num = match.attrib.get('mnum')
        state = ""
        status = ""
        toss = ""
        decision = ""
        title = match.attrib.get('srs')
        for st in match.iter('state'):
            state = st.attrib.get('mchState')
            status = st.attrib.get('status')
            toss = st.attrib.get('TW')
            decision = st.attrib.get('decisn')
        state_ob = CM.State(state, status, toss, decision)
        for score_item in match.iter('mscr'):
            crr = score_item.find('inngsdetail').attrib.get('crr')
            partnership = score_item.find('inngsdetail').attrib.get('cprtshp')
            batting = ""
            bowling = ""
            runs=""
            overs=""
            wickets=""
            inning = ""
            for batting_team in score_item.iter('btTm'):
                batting = batting_team.attrib.get("sName")
                for innings in batting_team.iter('Inngs'):
                    inning = innings.attrib.get('desc')
                    runs = innings.attrib.get('r')
                    overs = innings.attrib.get('ovrs')
                    wickets = innings.attrib.get('wkts')

            for bowling_team in score_item.iter('blgTm'):
                bowling = bowling_team.attrib.get('sName')
            scorecard = CM.ScoreCard(batting, bowling, partnership, runs, overs, wickets, inning, crr)
            match_ob = CM.Match( title, match.attrib.get('id'), match.attrib.get('type'), match_num, venue, state, scorecard)
            gv.matches[match_ob.identifier] = match_ob





def scrape():
    print("In scrape")
    live_matches_urls = []
    live_matches_titles = []
    gv.current_stats_str=""
    try:
        page = requests.get(gv.LIVE_MATCHES_URL)
        if page.status_code!=200:
            raise ValueError("Could not connect to the webpage")
        soup = BS(page.content, 'html.parser')
        print("first for")
        print(soup.prettify())
        for anchor in soup.find_all('a', {'class': 'cb-mat-mnu-itm cb-ovr-flo'}):
            title = anchor['title']
            if title.split(" ")[-1:][0].lower() in gv.LIVE_IDENTIFIERS:
                print("title is ",title)
                live_matches_urls.append(anchor['href'])
                live_matches_titles.append(anchor['title'])

        for current_match in live_matches_urls:
            page = requests.get(gv.ROOT_URL+current_match)
            soup = BS(page.content, 'html.parser')
            print("first for")
            """
            for anchor in soup.find_all('a',{ 'href':re.compile("cricket-match-highlights/*")}):
                print("anchor ",anchor['href'])
                print(gv.ROOT_URL + anchor['href'])
                highlights_page = requests.get(gv.ROOT_URL + anchor['href'])
                highlights_soup = BS(highlights_page.content,'html.parser')

                print("THIS IS HIGHLIGHTS SOUP\n",highlights_soup.prettify())
            """

            #for fours_soup in soup.find_all('div',{'class':"cb-mat-mnu-wrp cb-ovr-num"}):
            #        print("Parents are ",fours_soup.parent.text)
            for fours_soup in soup.find_all('p',{'class':"cb-com-ln cb-col cb-col-90"}):
                    gv.current_stats_str+="\n"+fours_soup.parent.text.strip().split()[0]+fours_soup.parent.text
                    obj = over_summary(fours_soup.parent.text.strip().split()[0],fours_soup.parent.text,"")
                    gv.current_stats.append(obj)
                    print("text ",fours_soup.parent.text.strip().split(" ")[0])
            print("printing soup contents",soup.prettify())
    except ValueError as value_error:
        print(value_error.args)

    finally:
        print()
