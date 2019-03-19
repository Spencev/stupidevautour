import json
import profileManager as profile
import computer as computer

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
    return (playerPlayed / len(playerHand)) / (abs(lastCard) / len(negMiddleDeck))

def calcAggression(playerHand, playerPlayed, lastCard, posMiddleDeck):
    return (playerPlayed / len(playerHand)) / (lastCard / len(posMiddleDeck))

def updateAggression(playerHand, playerPlayed, lastCard, posMiddleDeck, userProfile):
    newToList = calcAggression(playerHand, playerPlayed, lastCard, posMiddleDeck)
    userProfile["aggressionList"].append(newToList)
    newRating = round(sum(userProfile["aggressionList"]) / float(len(userProfile["aggressionList"])), 3)
    userProfile["aggression"] = newRating

def updateAversion(playerHand, playerPlayed, lastCard, negMiddleDeck, userProfile):
    newToList = calcAversion(playerHand, playerPlayed, lastCard, posMiddleDeck)
    userProfile["aversionList"].append(newToList)
    newRating = round(sum(userProfile["aversionList"]) / float(len(userProfile["aversionList"])), 3)
    userProfile["aversion"] = newRating
    
def initialize():
    profileList = profile.loadProfiles()
    return profileList