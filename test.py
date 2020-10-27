import requests

BASE = "http://127.0.0.1:5000/"

response = requests.put(BASE + "/team/1", {"team_name" : "A", "coach_name" : "coach_A", "captain_name" : "captain_A"}
                        )
print(response.json())
# team with diff id but same name
response = requests.put(BASE + "/team/2", {"team_name" : "A", "coach_name" : "coach_A", "captain_name" : "captain_A"}
                        )
print(response.json())
# team with diff if and diff name
response = requests.put(BASE + "/team/2", {"team_name" : "B", "coach_name" : "coach_A", "captain_name" : "captain_A"}
                        )
print(response.json())
# team with same id but diff name
response = requests.put(BASE + "/team/2", {"team_name" : "C", "coach_name" : "coach_A", "captain_name" : "captain_A"}
                        )
print(response.json())
# team with diff id and diff name
response = requests.put(BASE + "/team/3", {"team_name" : "C", "coach_name" : "coach_A", "captain_name" : "captain_A"}
                        )
print(response.json())

response = requests.put(BASE + "/match/1", {
    'date' : "27/10/2020",
    'team_1' : "A",
    'team_2' : "B",
    'runs_by_1' : 120,
    'runs_by_2' : 130,
    'wickets_lost_1' : 2,
    'wickets_lost_2' : 7,
    'fours_by_1' : 7,
    'fours_by_2' : 3,
    'sixes_by_1' : 3,
    'sixes_by_2' : 4,
    'outcome' : 1,
    'motm' : "Snigdha Singh",
    'overs' : 20
})

print(response.json())

response = requests.put(BASE + "/match/2", {
    'date' : "26/10/2020",
    'team_1' : "A",
    'team_2' : "B",
    'runs_by_1' : 120,
    'runs_by_2' : 130,
    'wickets_lost_1' : 2,
    'wickets_lost_2' : 7,
    'fours_by_1' : 7,
    'fours_by_2' : 3,
    'sixes_by_1' : 3,
    'sixes_by_2' : 4,
    'outcome' : 1,
    'motm' : "Snigdha Singh",
    'overs' : 20
})

print(response.json())

response = requests.get(BASE + "/matches")
print(response.json())

# team exists, get details
response = requests.get(BASE + "/team/2")
print(response.json())

# team does not exist
response = requests.get(BASE + "/team/4")
print(response.json())

# match exists
response = requests.get(BASE + "/match/1")
print(response.json())

# match does not exist
response = requests.get(BASE + "/match/5")
print(response.json())
