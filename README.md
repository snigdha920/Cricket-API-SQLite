# Cricket API 

Built using Flask & SQLite

# Features

1. Get all matches from database

2. Get a match's details

3. Add a team

4. Add a match

# Usage 

1. http://127.0.0.1:5000/matches

This endpoint will return list of matches with details 
- Teams who participated 
- Winner
- Team X won by A runs / wickets

2. Put request at : http://127.0.0.1:5000/team/{team_id}

This endpoint is used to add a team having details
- Team ID (primary key)
- Team name
- Captain name
- Coach name
- Matches played till date

3. Get request at : http://127.0.0.1:5000/team/{team_id}

This endpoint is used to get a team having details 
- Team ID (primary key)
- Team name
- Captain name
- Coach name
- Matches played till date

4. Put request at : http://127.0.0.1:5000/match/{match_id}

This endpoint is used to add a match having details 
- Teams who participated 
- Winner
- Match ID of the match
- Runs scored by each team
- Fours scored by each team
- Sixes scored by each team
- Wickets lost by each team
- Overs played in the match

5. Get request at : http://127.0.0.1:5000/match/{match_id}

This endpoint is used to get the following details of a match having id = match_id -
- Teams who participated 
- Winner
- Match ID of the match
- Runs scored by each team
- Fours scored by each team
- Sixes scored by each team
- Wickets lost by each team
- Overs played in the match
- Details of teams that participated such as team name, coach name, captain name, number of matches played till date

# How to use

1. Download the code
2. Install the requirements by running pip install -r requirements.txt
3. Run server by python app.py
