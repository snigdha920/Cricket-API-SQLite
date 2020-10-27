import datetime
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_restful.fields import DateTime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' 
db = SQLAlchemy(app)

# request parser for adding teams
team_details = reqparse.RequestParser()
team_details.add_argument("team_name", type = str, required = True, help = "Team name is required")
team_details.add_argument("coach_name", type = str, help = "Coach name")
team_details.add_argument("captain_name", type = str, required = True, help = "Captain name is required")
team_details.add_argument("matches_played", type = int, help = "Matches played till date")

# request parser for adding match
match_details = reqparse.RequestParser()
match_details.add_argument("date", type = str, help = "Date on which match was played is required...", required = True)
match_details.add_argument("team_1", type = str, help = "Name of team 1 is required...", required = True)
match_details.add_argument("team_2", type = str, help = "Name of team 2 is required...", required = True)
match_details.add_argument("runs_by_1", type = int, help = "Runs by team 1 is required...", required = True)
match_details.add_argument("runs_by_2", type = int, help = "Runs by team 2 is required...", required = True)
match_details.add_argument("wickets_lost_1", type = int, help = "Wickets lost by team 1")
match_details.add_argument("wickets_lost_2", type = int, help = "Wickets lost by team 2")
match_details.add_argument("fours_by_1", type = int, help = "Fours scored by team 1")
match_details.add_argument("fours_by_2", type = int, help = "Fours scored by team 2")
match_details.add_argument("sixes_by_1", type = int, help = "Sixes scored by team 1")
match_details.add_argument("sixes_by_2", type = int, help = "Sixes scored by team 2")
match_details.add_argument("outcome", type = str, help = "Outcome of the match is required...", required = True)
match_details.add_argument("motm", type = str, help = "Man of the match is required...", required = True)
match_details.add_argument("overs", type = int, help = "Number of overs played in the match is required...", required = True)

class TeamsModel(db.Model):
    __table_name__ = "Teams"
    __table_args__ = (
        db.UniqueConstraint('team_name'),
    ) # team name must be unique
    id = db.Column(db.Integer, primary_key = True)
    team_name = db.Column(db.Integer, nullable = False)
    coach_name = db.Column(db.String(255), nullable = True)
    captain_name = db.Column(db.String(255), nullable = False)
    matches_played = db.Column(db.Integer, default = 0)

    # representation function
    def __repr__(self):
        return f"Team: {self.id} :- Team name: {self.team_name}, Coach name: {self.coach_name}, Captain name: {self.captain_name}"

class MatchModel(db.Model):
    __table_name__ = "Match"
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, nullable = False)
    team_1 = db.Column(db.String, nullable = False)
    team_2 = db.Column(db.String, nullable = False)
    runs_by_1 = db.Column(db.Integer, nullable = False)
    runs_by_2 = db.Column(db.Integer, nullable = False)
    wickets_lost_1 = db.Column(db.Integer, default = 0)
    wickets_lost_2 = db.Column(db.Integer, default = 0)
    fours_by_1 = db.Column(db.Integer, default = 0)
    fours_by_2 = db.Column(db.Integer, default = 0)
    sixes_by_1 = db.Column(db.Integer, default = 0)
    sixes_by_2 = db.Column(db.Integer, default = 0)
    outcome = db.Column(db.Integer, nullable = False) # 3 if draw
    motm = db.Column(db.String, nullable = False)
    overs = db.Column(db.Integer, nullable = False)

db.drop_all()
db.create_all()

team_resource_fields = {
    'id' : fields.Integer,
    'team_name' : fields.String,
    'coach_name' : fields.String,
    'captain_name' : fields.String
}

match_resource_fields = {
    'id': fields.Integer,
    'date' : fields.DateTime,
    'team_1' : fields.String,
    'team_2' : fields.String,
    'runs_by_1' : fields.Integer,
    'runs_by_2' : fields.Integer,
    'wickets_lost_1' : fields.Integer,
    'wickets_lost_2' : fields.Integer,
    'fours_by_1' : fields.Integer,
    'fours_by_2' : fields.Integer,
    'sixes_by_1' : fields.Integer,
    'sixes_by_2' : fields.Integer,
    'outcome' : fields.Integer,
    'motm' : fields.String,
    'overs' : fields.Integer
}

def verifyRuns(runs, fours, sixes):
    if runs < 4*fours or runs < 6*sixes or runs < (4*fours + 6*sixes) :
        return 0
    return 1

class Team(Resource):

    @marshal_with (team_resource_fields) # to serialise new_team TeamsModel object
    def put(self, team_id):
        args = team_details.parse_args()
        check = TeamsModel.query.filter_by(id = team_id).first()
        if check : 
            abort(404, message = "Team with given ID already exists...")
        check = TeamsModel.query.filter_by(team_name = args['team_name']).first()
        if check :
            abort(404, message = "Team with given name already exists...")
        new_team = TeamsModel(id = team_id, team_name = args['team_name'], coach_name = args['coach_name'], captain_name = args['captain_name'], matches_played = args['matches_played'])
        db.session.add(new_team)
        db.session.commit()
        return new_team

    def get(self, team_id):
        check = TeamsModel.query.filter_by(id = team_id).first()
        if not check :
            abort(404, message = "Team does not exist")
        team = {}
        team['team name'] = check.team_name
        team['coach name'] = check.coach_name
        team['captain name'] = check.captain_name
        team['matches played'] = check.matches_played
        return team

class Match(Resource):

    @marshal_with (match_resource_fields)
    def put(self, match_id):
        args = match_details.parse_args()
        check = MatchModel.query.filter_by(id = match_id).first()
        if check :
            abort(404, message = "Match ID already exists...")
        date_time_obj = datetime.datetime.strptime(args['date'], '%d/%m/%Y')
        if not verifyRuns(args['runs_by_1'], args['fours_by_1'], args['sixes_by_1']):
            abort(404, message = "Invalid score of Team 1")
        if not verifyRuns(args['runs_by_2'], args['fours_by_2'], args['sixes_by_2']):
            abort(404, message = "Invalid score for Team 2")
        if args['wickets_lost_1'] > 11 :
            abort(404, message = "Invalid number of wickets lost by Team 1")
        if args['wickets_lost_2'] > 11 :
            abort(404, message = "Invalid number of wickets lost by Team 2")
        team1 = TeamsModel.query.filter_by(team_name = args['team_1']).first()
        if team1 :
            team1.matches_played += 1
        team2 = TeamsModel.query.filter_by(team_name = args['team_2']).first()
        if team2 :
            team2.matches_played += 1
        new_match = MatchModel(
            id = match_id,
            date = date_time_obj.date(),
            team_1 = args['team_1'],
            team_2 = args['team_2'],
            runs_by_1 = args['runs_by_1'],
            runs_by_2 = args['runs_by_2'],
            wickets_lost_1 = args['wickets_lost_1'],
            wickets_lost_2 = args['wickets_lost_2'],
            fours_by_1 = args['fours_by_1'],
            fours_by_2 = args['fours_by_2'],
            sixes_by_1 = args['sixes_by_1'],
            sixes_by_2 = args['sixes_by_2'],
            outcome = args['outcome'],
            motm = args['motm'],
            overs = args['overs']
        )
        db.session.add(new_match)
        db.session.commit()
        return new_match

    def get(self, match_id):
        match = MatchModel.query.filter_by(id = match_id).first()
        if not match :
            abort(404, message = "Invalid match ID...")
        tempMatch = {}
        tempMatch['team 1 name'] = match.team_1
        tempMatch['team 2 name'] = match.team_2
        if match.outcome == 1 :
            tempMatch['winner'] = match.team_1
        elif match.outcome == 2 :
            tempMatch['winner'] = match.team_2
        else :
            tempMatch['winner'] = "Match was drawn between " + match.team_1 + " " + match.team_2
            
        if tempMatch['winner'] is match.team_1 :
            if match.wickets_lost_1 == match.wickets_lost_2:
                tempMatch['details'] = match.team_1 + " won by " + str(match.runs_by_1 - match.runs_by_2) + " runs"
            else :
                tempMatch['details'] = match.team_1 + " won by " + str(match.wickets_lost_2 - match.wickets_lost_1) + " wickets"
        elif tempMatch['winner'] is match.team_2 :
            if match.wickets_lost_1 == match.wickets_lost_2:
                tempMatch['details'] = match.team_2 + " won by " + str(match.runs_by_2 - match.runs_by_1) + " runs"
            else :
                tempMatch['details'] = match.team_2 + " won by " + str(match.wickets_lost_1 - match.wickets_lost_2) + " wickets"
        else:
            tempMatch['details'] = "Match ended in a draw as score of both teams was " + str(match.runs_by_1) + "/" + str(match.wickets_lost_1)
        tempMatch['score of team 1'] = str(match.runs_by_1) + "/" + str(match.wickets_lost_1)
        tempMatch['score of team 2'] = str(match.runs_by_2) + "/" + str(match.wickets_lost_2)
        tempMatch['fours by team 1'] = match.fours_by_1
        tempMatch['sixes by team 1'] = match.sixes_by_1
        tempMatch['fours by team 2'] = match.fours_by_2
        tempMatch['sixes by team 2'] = match.sixes_by_2
        tempMatch['man of the match'] = match.motm
        check = TeamsModel.query.filter_by(team_name = match.team_1).first()
        if check :
            team = {}
            team['team name'] = check.team_name
            team['coach name'] = check.coach_name
            team['captain name'] = check.captain_name
            team['matches played'] = check.matches_played
            tempMatch['details of team 1: '] = team
        check = TeamsModel.query.filter_by(team_name = match.team_2).first()
        if check :
            team = {}
            team['team name'] = check.team_name
            team['coach name'] = check.coach_name
            team['captain name'] = check.captain_name
            team['matches played'] = check.matches_played
            tempMatch['details of team 2: '] = team
        return tempMatch

class Matches(Resource):

    def get(self):
        allMatches = {}
        matches = MatchModel.query.order_by('date').all()
        idx = 1
        for match in matches:
            tempMatch = {}
            tempMatch['team 1 name'] = match.team_1
            tempMatch['team 2 name'] = match.team_2

            if match.outcome == 1 :
                tempMatch['winner'] = match.team_1
            elif match.outcome == 2 :
                tempMatch['winner'] = match.team_2
            else :
                tempMatch['winner'] = "Match was drawn between " + match.team_1 + " " + match.team_2
            
            if tempMatch['winner'] is match.team_1 :
                if match.wickets_lost_1 == match.wickets_lost_2:
                    tempMatch['details'] = match.team_1 + " won by " + str(match.runs_by_1 - match.runs_by_2) + " runs"
                else :
                    tempMatch['details'] = match.team_1 + " won by " + str(match.wickets_lost_2 - match.wickets_lost_1) + " wickets"
            elif tempMatch['winner'] is match.team_2 :
                if match.wickets_lost_1 == match.wickets_lost_2:
                    tempMatch['details'] = match.team_2 + " won by " + str(match.runs_by_2 - match.runs_by_1) + " runs"
                else :
                    tempMatch['details'] = match.team_2 + " won by " + str(match.wickets_lost_1 - match.wickets_lost_2) + " wickets"
            else:
                tempMatch['details'] = "Match ended in a draw as score of both teams was " + str(match.runs_by_1) + "/" + str(match.wickets_lost_1)
            tempMatch['date'] = match.date.strftime('%d/%m/%Y')
            allMatches[idx] = tempMatch
            idx+=1
        return allMatches


api.add_resource(Team, "/team/<int:team_id>")
api.add_resource(Match, "/match/<int:match_id>")
api.add_resource(Matches, "/matches")

if __name__ == "__main__":
    app.run(debug=True)