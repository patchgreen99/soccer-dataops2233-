import json
import math


# frameData = json.loads(line['FrameData'])

# with open('oneFrame.json.json', 'r') as f:
#     dataMatch = json.load(f)
#     print(dataMatch)
#
def playerInPossession(data):
    frameCount = data['EXPR$1']
    frameData = json.loads(data['FrameData'])
    ballPosition = frameData[0]['BallPosition'][0]
    players = frameData[0]["PlayerPositions"]

    playersInThreshold = []

    if ballPosition['Speed'] < 15:
        # players = (frameData[0]["PlayerPositions"])
        for player in players:
            if math.sqrt(pow(player["X"] - ballPosition['X'], 2) + pow(player["Y"] - ballPosition['Y'], 2)) < 200:
                if len(playersInThreshold) < 1:
                    playersInThreshold.append([frameCount, player["JerseyNumber"], player["Team"]])
                else:
                    break

    if len(playersInThreshold) == 1:
        playerInPossession = {"frameCount": playersInThreshold[0][0], "JerseyNumber": playersInThreshold[0][1], "team": playersInThreshold[0][2]}
        return playerInPossession
    else:
        return {"frameCount": -1, "JerseyNumber": -1, "team": -1}


listOfPossessionInAMatch = []

with open('test.json', 'r') as f:
    for line in f:

        dataMatch = json.loads(line)
        # print()

        # print(dataMatch)
        possession = playerInPossession(dataMatch)
        if possession is not None:
            listOfPossessionInAMatch.append(possession)

print(listOfPossessionInAMatch)
print(len(listOfPossessionInAMatch))

team1 = 0
team0 = 0
noTeam = 0
for data in listOfPossessionInAMatch:
    team = data['team']
    if team == 1:
        team1 +=1
    elif team == 0:
        team0 +=1
    else:
        noTeam +=1

print(team1, team0, noTeam)

