import json
import math


def playersInPossession(data):
    frameData = json.loads(data['FrameData'])
    ballPosition = frameData[0]['BallPosition'][0]
    players = frameData[0]["PlayerPositions"]

    playersInThreshold = []

    if ballPosition['Speed'] < 15:
        for player in players:
            if player["Team"] == 1 or player["Team"] == 0:
                if math.sqrt(pow(player["X"] - ballPosition['X'], 2) + pow(player["Y"] - ballPosition['Y'], 2)) < 200:
                    playersInThreshold.append([player["JerseyNumber"], player["Team"]])

    if len(playersInThreshold) == 1:
        playerInPossession = {"JerseyNumber": playersInThreshold[0][0], "team": playersInThreshold[0][1]}
        return playerInPossession
    else:
        return None


listOfPossessionInAMatch = []
with open('fullMatch.json', 'r') as f:
    for line in f:

        dataMatch = json.loads(line)
        possession = playersInPossession(dataMatch)
        listOfPossessionInAMatch.append(possession)

# there is something wrong with it, as 'JerseyNumber': 22 is in possession of the ball most of the time
print("PossessionInFrameData ⚽")
print(listOfPossessionInAMatch)

listOfPossessionInEventData = []
with open('tracabEventLowLatency.json', 'r') as f:
    for line in f:
        dataMatch = json.loads(line)
        data = json.loads(dataMatch['data'])
        eventData = data['EventData']
        playerTeam = eventData.get('Team')
        playerJersey = eventData.get('PlayerJersey')
        confidence = eventData.get('Confidence')

        if playerTeam == 1 or playerTeam == 0:
            listOfPossessionInEventData.append({"JerseyNumber": playerJersey, "team": playerTeam})
        else:
            listOfPossessionInEventData.append(None)

print("PossessionInEventData 🏟️")
print(listOfPossessionInEventData)


def checkTeams(listOfData):
    teamHome = 0
    teamAway = 0
    noTeam = 0

    for data in listOfData:
        if data is not None:
            team = data['team']
            if team == 1:
                teamHome += 1
            elif team == 0:
                teamAway += 1
            else:
                noTeam += 1
        else:
            noTeam +=1
    return teamHome, teamAway, noTeam

# the away team possession are too different on both data
print("FrameData  ⚽")
print(checkTeams(listOfPossessionInAMatch))
print("EventData 🏟️")
print(checkTeams(listOfPossessionInEventData))

