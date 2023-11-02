import json
import math

with open('oneFrame.json', 'r') as f:
    dataMatch = json.load(f)
print(dataMatch)

frameData = json.loads(dataMatch['FrameData'])
ballPosition = frameData[0]['BallPosition'][0]

ballSpeed = ballPosition['Speed']
ballX = ballPosition['X']
ballY = ballPosition['Y']

print(ballX)
print(ballY)
print(ballSpeed)

playersInThreshold = []

if ballSpeed < 15:
    players = (frameData[0]["PlayerPositions"])
    for player in players:
        jerseyNumber = player["JerseyNumber"]
        team = player["Team"]
        playerX = player["X"]
        playerY = player["Y"]

        if math.sqrt(pow(playerX-ballX, 2) + pow(playerY-ballY, 2)) < 200:
            playersInThreshold.append([jerseyNumber, team])

print(playersInThreshold)
