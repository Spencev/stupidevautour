import json
import profileManager as profile

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
        percentMatrix.append([round((winCount/15)*100, 2), round((tieCount/15)*100, 2), round((loseCount/15)*100, 2)])
    return percentMatrix

#ex1 = generatePercents([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
#print(ex1)
    
def calcAversion(playerHand, playerPlayed, lastCard, negMiddleDeck):
    return abs(playerPlayed * (playerHand.index(playerPlayed) / len(playerHand)) * lastCard * (negMiddleDeck.index(lastCard) / len(negMiddleDeck)) * (playerPlayed - abs(lastCard)))

def calcAggression(playerHand, playerPlayed, lastCard, posMiddleDeck):
    return playerPlayed * (playerHand.index(playerPlayed) / len(playerHand)) * lastCard * (posMiddleDeck.index(lastCard) / len(posMiddleDeck)) * (playerPlayed - lastCard)

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