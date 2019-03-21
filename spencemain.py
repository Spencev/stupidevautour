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

def updateAggression(playerHand, playerPlayed, lastCard, posMiddleDeck, userProfile):
    newToList = calcAggression(playerHand, playerPlayed, lastCard, posMiddleDeck)
    userProfile["aggressionList"].append(newToList)
    newRating = round(sum(userProfile["aggressionList"]) / float(len(userProfile["aggressionList"])), 3)
    if newRating > 2:
        newRating = 2
    userProfile["aggression"] = newRating

def updateAversion(playerHand, playerPlayed, lastCard, negMiddleDeck, userProfile):
    newToList = calcAversion(playerHand, playerPlayed, lastCard, negMiddleDeck)
    userProfile["aversionList"].append(newToList)
    newRating = round(sum(userProfile["aversionList"]) / float(len(userProfile["aversionList"])), 3)
    if newRating > 1.5:
        newRating = 1.5
    userProfile["aversion"] = newRating
    
def initialize():
    profileList = profile.loadProfiles()
    return profileList

def buildList(bidDict, compHand):
    bidList = []
    for card in bidDict:
        if card > 5:
            bidList.append([card, [card + 5]])
        else:
            toAdd = []
            if (abs(card) + abs(card)) in compHand:
                toAdd.append((abs(card)) + abs(card))
            if (abs(card) + abs(card) - 1) in compHand:
                toAdd.append((abs(card)) + abs(card) - 1)
            bidList.append([card, toAdd])
    return bidList

def decide(playerHand, compHand, participant, currentBid, bidDict):
    if len(compHand) == 1:
        return 1
    if currentBid == bidDict[-1]:
        percentMatrix = generatePercents(playerHand, compHand)
        for row in percentMatrix:
            if row == len(compHand):
                return compHand[percentMatrix.index(row)]
        if random.random() < participant[2] and max(playerHand) > max(compHand):
            return 1
        else:
            return 0
    print(bidDict)
    bidList = buildList(bidDict, compHand)
    print(bidList)
    for bid in bidList:
        print("currentBid: " + str(currentBid))
        print("compHand: " + str(compHand))
        print("bid: " + str(bid))
        if bid[0] == currentBid:
            print("true")
            if len(bid[1]) != 0:
                result = random.choice(bid[1])
                break
            if currentBid > 0:
                if participant[0] > 1:
                    count = 1
                    while True:
                        if result + count in compHand:
                            result = result + count
                            print("twio" + str(result))
                            break
                        if result - (count + 1) in compHand:
                            result = result - (count + 1)
                            print("three " + str(result))
                            break
                        count += 1
                if participant[0] <= 1:
                    count = 1
                    while True:
                        if result - count in compHand:
                            result = result - count
                            print("four " + str(result))
                            break
                        if result + (count + 1) in compHand:
                            result = result + (count + 1)
                            print("five " + str(result))
                            break
                        count += 1
            else:
                if participant[1] > 0.75:
                    count = 1
                    while True:
                        if result + count in compHand:
                            result = result + count
                            print("six " + str(result))
                            break
                        if result - (count + 1) in compHand:
                            result = result - (count + 1)
                            print("seven " + str(result))
                            break
                        count += 1
                if participant[1] <= 0.75:
                    count = 1
                    while True:
                        if result - count in compHand:
                            result = result - count
                            print("eight " + str(result))
                            break
                        if result + (count + 1) in compHand:
                            result = result + (count + 1)
                            print("nine " + str(result))
                            break
                        count += 1
            for bidValue in bidList:
                if result in bidValue[1]:
                    bidValue[1].remove(result)
            break
    print(result)
    return compHand.index(result)
