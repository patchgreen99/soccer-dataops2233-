import json
import math


def playersInPossession(data):
    frameCount = data['EXPR$1']
    frameData = json.loads(data['FrameData'])
    ballPosition = frameData[0]['BallPosition'][0]
    players = frameData[0]["PlayerPositions"]

    playersInThreshold = []

    if ballPosition['Speed'] < 15:
        for player in players:
            if player["Team"] == 1 or player["Team"] == 0:
                if math.sqrt(pow(player["X"] - ballPosition['X'], 2) + pow(player["Y"] - ballPosition['Y'], 2)) < 200:
                    playersInThreshold.append([frameCount, player["JerseyNumber"], player["Team"]])

    if len(playersInThreshold) == 1:
        playerInPossession = {"frameCount": playersInThreshold[0][0], "JerseyNumber": playersInThreshold[0][1], "team": playersInThreshold[0][2]}
        return playerInPossession
    else:
        return None


listOfPossessionInAMatch = []
teamHome = 0
teamAway = 0
noTeam = 0

with open('fullMatch.json', 'r') as f:
    for line in f:

        dataMatch = json.loads(line)
        possession = playersInPossession(dataMatch)

        if possession is None:
            noTeam +=1
        else:
            listOfPossessionInAMatch.append(possession)

for data in listOfPossessionInAMatch:
    team = data['team']
    if team == 1:
        teamHome += 1
    elif team == 0:
        teamAway += 1

print(teamHome, teamAway, noTeam)


