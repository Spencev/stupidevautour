import json
import profileManager as profile
import random

def generatePercents(playerHand, compHand):
    percentMatrix = []
    for compCard in compHand:
        winCount = 0
        tieCount = 0
        loseCount = 0
        for playerCard in playerHand:
            if compCard > playerCard:
                winCount += 1
            if compCard == playerCard:
                tieCount += 1
            if compCard < playerCard:
                loseCount += 1
        percentMatrix.append([round((winCount/len(compHand))*100, 2), round((tieCount/len(compHand))*100, 2), round((loseCount/len(compHand))*100, 2)])
    return percentMatrix
    
def calcAversion(playerHand, playerPlayed, lastCard, negMiddleDeck):
    return ((playerHand.index(playerPlayed) + 1) / len(playerHand)) / ((negMiddleDeck.index(lastCard) + 1) / len(negMiddleDeck))

def calcAggression(playerHand, playerPlayed, lastCard, posMiddleDeck):
    return ((playerHand.index(playerPlayed) + 1) / len(playerHand)) / ((negMiddleDeck.index(lastCard) + 1) / len(posMiddleDeck))

def updateAggression(playerHand, playerPlayed, lastCard, posMiddleDeck, userProfile):
    newToList = calcAggression(playerHand, playerPlayed, lastCard, posMiddleDeck)
    userProfile["aggressionList"].append(newToList)
    newRating = round(sum(userProfile["aggressionList"]) / float(len(userProfile["aggressionList"])), 3)
    userProfile["aggression"] = newRating

def updateAversion(playerHand, playerPlayed, lastCard, negMiddleDeck, userProfile):
    newToList = calcAversion(playerHand, playerPlayed, lastCard, negMiddleDeck)
    userProfile["aversionList"].append(newToList)
    newRating = round(sum(userProfile["aversionList"]) / float(len(userProfile["aversionList"])), 3)
    userProfile["aversion"] = newRating
    
def initialize():
    profileList = profile.loadProfiles()
    return profileList

def rescale(validList, attribute, isAggression):
    

def decide(playerHand, compHand, participant, currentBid, bidDict):
    print(playerHand)
    print(compHand)
    print(participant)
    print(currentBid)
    print(bidDict)
    percentMatrix = generatePercents(playerHand, compHand)
    if currentBid == 10:
        for row in percentMatrix:
            if row[0] == 100:
                return compHand[percentMatrix.index(row)]
        if random.ramdom() < particpant[2]:
            return compHand[0]
    if currentBid > 0:
        posMiddleDeck = []
        for card in bidDict:
            if card > 0:
                posMiddleDeck.append(card)
        validList = []
        for card in compHand:
            validList.append(calcAggression(compHand, card, currentBid, posMiddleDeck))
        rescaledAggression = rescale(validList, participant[0], True)
        return compHand.index(round(len(compHand) * (rescaledAggression * ((posMiddleDeck.index(currentBid) + 1) / len(posMiddleDeck)))))
    if currentBid < 0:
        negMiddleDeck = []
        for card in bidDict:
            if card < 0:
                negMiddleDeck.append(card)
        validList = []
        for card in compHand:
            validList.append(calcAversion(compHand, card, currentBid, negMiddleDeck))
        rescaledAversion = rescale(validList, participant[1], False)
        return compHand.index(round(len(compHand) * (rescaledAversion * ((negMiddleDeck.index(currentBid) + 1) / len(negMiddleDeck)))))