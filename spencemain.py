import profileManager as profile
import random
import numpy as np

def generatePercents(playerHand, compHand): #generate the percent matrix to figure out if the participant has a 100 percent chance of wining and at what cards
    percentMatrix = []
    for compCard in compHand:#iterate through
        winCount = 0
        for playerCard in playerHand:
            if compCard > playerCard:#winning card
                winCount += 1
        percentMatrix.append(winCount)
    return percentMatrix
    
def calcAversion(playerHand, playerPlayed, lastCard, negMiddleDeck): #aversion calculation which outlined in the report
    return ((playerHand.index(playerPlayed) + 1) / len(playerHand)) / ((negMiddleDeck.index(lastCard) + 1) / len(negMiddleDeck))

def calcAggression(playerHand, playerPlayed, lastCard, posMiddleDeck): #aggression calculation which outlined in the report
    return ((playerHand.index(playerPlayed) + 1) / len(playerHand)) / ((posMiddleDeck.index(lastCard) + 1) / len(posMiddleDeck))

def calcDeception(playerHand, compHand, playerPlayed, lastCard): #deception calculation which outlined in the report
    percentMatrix = generatePercents(playerHand, compHand)
    topCards = []
    for row in percentMatrix:
        if row == 100:
            topCards.append(percentMatrix.index(row))
    if playerHand.index(playerPlayed) in topCards:
        return 1
    else:
        return 0

def updateAggression(playerHand, playerPlayed, lastCard, posMiddleDeck, userProfile): #updating the players profile for aggression
    newToList = calcAggression(playerHand, playerPlayed, lastCard, posMiddleDeck)
    userProfile["aggressionList"].append(round(newToList, 3))
    newRating = round(sum(userProfile["aggressionList"]) / float(len(userProfile["aggressionList"])), 3)
    if newRating > 2:
        newRating = 2
    userProfile["aggression"] = newRating

def updateAversion(playerHand, playerPlayed, lastCard, negMiddleDeck, userProfile):#updating the players profile for aversion
    newToList = calcAversion(playerHand, playerPlayed, lastCard, negMiddleDeck)
    userProfile["aversionList"].append(round(newToList, 3))
    newRating = round(sum(userProfile["aversionList"]) / float(len(userProfile["aversionList"])), 3)
    if newRating > 1.5:
        newRating = 1.5
    userProfile["aversion"] = newRating
    
def updateDeception(playerHand, playerPlayed, compHand, lastCard, userProfile): #updating the players profile for deception
    newToList = calcDeception(playerHand, compHand, playerPlayed, lastCard)
    userProfile["deceptionList"].append(round(newToList, 3))
    newRating = round(sum(userProfile["deceptionList"]) / float(len(userProfile["deceptionList"])), 3)
    userProfile["deception"] = newRating
    
def convertAttribute(value): #conversion scale for attribute to modifier on baseline scale, explained in report as well
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
    
def initialize(): #load in the profiles
    profileList = profile.loadProfiles()
    return profileList

def decide(playerHand, compHand, participant, currentBid, bidDict): #picks the card 
    if len(compHand) == 1: #no decision to be made, picks the only card in hand
        return 0
    if currentBid == bidDict[-1]:#deception situation explained in report
        percentMatrix = generatePercents(playerHand, compHand)
        for row in percentMatrix:
            if row == len(compHand):
                return percentMatrix.index(row) #not deceiving 
        if random.random() < participant[2] and max(playerHand) > max(compHand): #deceiving 
            return 0
    bidList = [[-5, [10, 9]], [-4, [8, 7]], [-3, [6, 5]], [-2, [4, 3]], [-1, [2, 1]], [1, [2, 1]], [2, [4, 3]], [3, [6, 5]], [4, [8, 7]], [5, [9, 10]], [6, [11]], [7, [12]], [8, [13]], [9, [14]], [10, [15]]] #baseline scale explained in report
    for bid in bidList: #iterate through to find current build
        if bid[0] == currentBid:
            for suggested in bid[1]:
                if currentBid > 0: #aggression
                    if suggested + convertAttribute(participant[0]) in compHand: #looking if the modified value from the baseline scale is in the hand
                        return compHand.index(suggested + convertAttribute(participant[0]))
                if currentBid < 0: #aversion
                    if suggested + convertAttribute(participant[1]) in compHand: #looking if the modified value from the baseline scale is in the hand
                        return  compHand.index(suggested + convertAttribute(participant[1]))
            result = random.choice(bid[1]) #picking a starting point to explore for if the card picked was not in hand to find the closest one 
            if currentBid > 0:
                if participant[0] > 1: #explore upwards first 
                    count = 1
                    while True: #finding the closest card to be played by alternating up and down exploration 
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
                if participant[0] <= 1: #explore downwards first
                    count = 1
                    while True: #finding the closest card to be played by alternating up and down exploration 
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
                if participant[1] > 0.75: #explore upwards first 
                    count = 1
                    while True: #finding the closest card to be played by alternating up and down exploration 
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
                if participant[1] <= 0.75: #explore downwards first
                    count = 1
                    while True: #finding the closest card to be played by alternating up and down exploration 
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
    return compHand.index(result) #return the card