class Venue:
    def __init__(self, ground, city, country):
        self.ground = ground
        self.city = city
        self.country = country


class ScoreCard:
    def __init__(self, batting, bowling, partnership, runs, overs, wickets, innings, crr):
        self.batting = batting
        self.bowling = bowling
        self.partnership = partnership
        self.runs = runs
        self.overs = overs
        self.wickets = wickets
        self.innings = innings
        self.crr = crr


class State:
    def __init__(self, state, status, toss, decision):
        self.state = state
        self.status = status
        self.toss = toss
        self. decision = decision


class Match:
    def __init__(self, title, identifier, type_match, match_num, venue, state, scorecard):
        self.title = title
        self.identifier = identifier
        self.type_match = type_match
        self.match_num = match_num
        self.venue = venue
        self.state = state
        self.scorecard = scorecard