import json
import profileManager as profile
import random
import numpy as np
import bisect

def generatePercents(playerHand, compHand):
    percentMatrix = []
    for compCard in compHand:
        winCount = 0
        for playerCard in playerHand:
            if compCard > playerCard:
                winCount += 1
        percentMatrix.append(winCount)
    return percentMatrix
    
def calcAversion(playerHand, playerPlayed, lastCard, negMiddleDeck):
    return ((playerHand.index(playerPlayed) + 1) / len(playerHand)) / ((negMiddleDeck.index(lastCard) + 1) / len(negMiddleDeck))

def calcAggression(playerHand, playerPlayed, lastCard, posMiddleDeck):
    return ((playerHand.index(playerPlayed) + 1) / len(playerHand)) / ((posMiddleDeck.index(lastCard) + 1) / len(posMiddleDeck))

def calcDeception(playerHand, compHand, playerPlayed, lastCard, middleDeck):
    percentMatrix = generatePercents(playerHand, compHand)
    topCards = []
    for row in percentMatrix:
        if row == 100:
            topCards.append(percentMatrix.index(row))
    if playerHand.index(playerPlayed) in topCards:
        return 0
    else:
        return 1

def updateAggression(playerHand, playerPlayed, lastCard, posMiddleDeck, userProfile):
    newToList = calcAggression(playerHand, playerPlayed, lastCard, posMiddleDeck)
    userProfile["aggressionList"].append(round(newToList, 3))
    newRating = round(sum(userProfile["aggressionList"]) / float(len(userProfile["aggressionList"])), 3)
    if newRating > 2:
        newRating = 2
    userProfile["aggression"] = newRating

def updateAversion(playerHand, playerPlayed, lastCard, negMiddleDeck, userProfile):
    newToList = calcAversion(playerHand, playerPlayed, lastCard, negMiddleDeck)
    userProfile["aversionList"].append(round(newToList, 3))
    newRating = round(sum(userProfile["aversionList"]) / float(len(userProfile["aversionList"])), 3)
    if newRating > 1.5:
        newRating = 1.5
    userProfile["aversion"] = newRating
    
def updateDeception(playerHand, playerPlayed, compHand, lastCard, userProfile):
    newToList = calcDeception(playerHand, compHand, playerPlayed, lastCard, middleDeck)
    userProfile["deceptionList"].append(round(newToList, 3))
    newRating = round(sum(userProfile["deceptionList"]) / float(len(userProfile["deceptionList"])), 3)
    userProfile["deception"] = newRating
    
def convertAttribute(value):
    if value < 0.25:
        return -3
    if value < 0.5:
        return -2
    if value < 0.9:
        return -1
    if value < 1.1:
        return 0
    if value < 1.5:
        return 1
    if value < 1.75:
        return 2
    if value < 2:
        return 3
    else:
        return 4
    
def initialize():
    profileList = profile.loadProfiles()
    return profileList

def decide(playerHand, compHand, participant, currentBid, bidDict):
    if len(compHand) == 1:
        return 0
    if currentBid == bidDict[-1]:
        percentMatrix = generatePercents(playerHand, compHand)
        for row in percentMatrix:
            if row == len(compHand):
                return percentMatrix.index(row)
        if random.random() < participant[2] and max(playerHand) > max(compHand):
            return 0
    bidList = [[-5, [10, 9]], [-4, [8, 7]], [-3, [6, 5]], [-2, [4, 3]], [-1, [2, 1]], [1, [2, 1]], [2, [4, 3]], [3, [6, 5]], [4, [8, 7]], [5, [9, 10]], [6, [11]], [7, [12]], [8, [13]], [9, [14]], [10, [15]]]
    for bid in bidList:
        if bid[0] == currentBid:
            countLimit = 0
            for suggested in bid[1]:
                countLimit += 1
                if currentBid > 0:
                    if suggested + convertAttribute(participant[0]) in compHand:
                        return compHand.index(suggested + convertAttribute(participant[0]))
                if currentBid < 0:
                    if suggested + convertAttribute(participant[1]) in compHand:
                        return  compHand.index(suggested + convertAttribute(participant[1]))
            result = random.choice(bid[1])
            if currentBid > 0:
                if participant[0] > 1:
                    count = 1
                    while True:
                        if result + count in compHand:
                            result = result + count
                            break
                        if result - (count + 1) in compHand:
                            result = result - (count + 1)
                            break
                        if result + count > max(compHand):
                            result = max(compHand)
                            break
                        if result - (count + 1) < min(compHand):
                            result = min(compHand)
                            break
                        count += 1
                if participant[0] <= 1:
                    count = 1
                    while True:
                        if result - count in compHand:
                            result = result - count
                            break
                        if result + (count + 1) in compHand:
                            result = result + (count + 1)
                            break
                        if result - count < min(compHand):
                            result = min(compHand)
                            break
                        if result + (count + 1) > max(compHand):
                            result = max(compHand)
                            break
                        count += 1
            else:
                if participant[1] > 0.75:
                    count = 1
                    while True:
                        if result + count in compHand:
                            result = result + count
                            break
                        if result - (count + 1) in compHand:
                            result = result - (count + 1)
                            break
                        if result + count > max(compHand):
                            result = max(compHand)
                            break
                        if result - (count + 1) < min(compHand):
                            result = min(compHand)
                            break
                        count += 1
                if participant[1] <= 0.75:
                    count = 1
                    while True:
                        if result - count in compHand:
                            result = result - count
                            break
                        if result + (count + 1) in compHand:
                            result = result + (count + 1)
                            break
                        if result - count < min(compHand):
                            result = min(compHand)
                            break
                        if result + (count + 1) > max(compHand):
                            result = max(compHand)
                            break
                        count += 1
    return compHand.index(result)