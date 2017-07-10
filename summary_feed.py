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




