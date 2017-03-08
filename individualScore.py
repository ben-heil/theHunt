#!/bin/python

import sys
import requests
import json
import argparse

def parsePlayers(playerFile):
    players = {}
    for line in playerFile:
        line = line.strip()
        players[line] = 0
    return players

#Read in rubric file name and gives help if necessary
parser = argparse.ArgumentParser(description = "Reads in scores for challenges, and calculates the score for each team")
parser.add_argument('tokenFile', help = "Location of the file containing user's token")
parser.add_argument('rubric', help = "Location of the file containing the rubric")
parser.add_argument('playerFile', help = "List of the hashtags of each player")
args = parser.parse_args()

#Open the rubric file
rubricFile = open(args.rubric)

playerFile = open(args.playerFile)
playerScores = parsePlayers(playerFile)

challenges = {}
#Read through the rubric file. Read in each challenge
for line in rubricFile:
    words = line.strip().split()
    if len(words) != 2:
        continue
    challenges[words[0]] = words[1]
#Ensure there is a file called token.txt in the same directory as the script
#This token holds a user token from the 
keyFile = open(args.tokenFile)

#Read in the Facebook access token
key = keyFile.readline().strip()

#This is the facebook id for the page node of The Hunt. 
#It is findable with the Facebook Graph Explorer, or by pulling from the URL
pageId = "255207594904623"

#Ask facebook to pull all posts from the hunt (up to 7000)
#In the future this can be implemented more efficiently with cursor based pagination
response = requests.post("https://graph.facebook.com/v2.8/"+ pageId +"?fields=feed.limit(7000)&method=get&access_token=" + key).json()

#Read through each message, and look at which hashtags it has
for item in response["feed"]["data"]:
    if "message" in item:
        for challenge in challenges:
            if item["message"].lower().find(challenge) != -1:
                for player in playerScores:
                    if item["message"].lower().find(player) != -1:
                        playerScores[player] += int(challenges[challenge])

#Print each player's score
for player in playerScores:
    print(player + '\t' + str(playerScores[player]))
    print("")
