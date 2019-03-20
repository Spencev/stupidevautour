import random
import spencemain as utility
import profileManager as profile
import numpy as np

def setParticipants(amount):
    participantList = []
    for participant in range(0, amount):
        participantList.append([round(random.uniform(0.1031, 2), 4), round(random.uniform(0.07784, 1.5), 4), random.random()])
    return participantList

def playGame(participant1, participant2):
    hand1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    hand2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    score1 = 0
    score2 = 0
    middleDeck = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    while len(middleDeck) > 0:
        currentBid = random.choice(middleDeck)
        hand1Choice = utility.decide(hand1, hand2, participant1, currentBid, middleDeck)
        hand2Choice = utility.decide(hand2, hand1, participant2, currentBid, middleDeck)
        hand1.remove(hand1Choice)
        hand2.remove(hand2Choice)
        middleDeck.remove(currentBid)
        if currentBid > 0:
            if hand1Choice > hand2Choice:
                score1 += currentBid
            elif hand2Choice > hand1Choice:
                score2 += currentBid
            else:
                continue
        if currentBid < 0:
            if hand1Choice > hand2Choice:
                score2 += currentBid
            elif hand2Choice > hand1Choice:
                score1 += currentBid
            else:
                continue
    if score1 > score2:
        return [1, score1 - score2]
    elif score1 < score2:
        return [-1, score1 - score2]
    else:
        return [0, 0]

def sumScores(compStatsList):
    scoreList = []
    for stat in compStatsList:
        score = 0
        for game in stat:
            score += (game[0] * 30) + game[1]
        scoreList.append(score)
    return stat[0][1] + stat[1][1] + stat[2][1]

def alterPool(participantList, compStatsList):
    scoreList = sumScores(compStatsList)
    medianScore = np.percentile(scoreList, 50)
    bottomQuarterScore = np.percentile(scoreList, 25)
    topQuarterScore = np.percentile(scoreList, 75)
    indexCount = 0
    topOfPool = []
    for score in scoreList:
        if score > topQuarterScore:
            topOfPool.append(participantList[indexCount])
        indexCount += 1
    indexCount = 0
    for score in scoreList:
        if score > medianScore:
            continue
        if score <= medianScore and score > bottomQuarterScore:
            exemplar = random.choice(topOfPool)
            participantList[indexCount][0] = ((participantList[indexCount][0] * 3) + exemplar[0]) / 4
            participantList[indexCount][1] = ((participantList[indexCount][1] * 3) + exemplar[1]) / 4
            participantList[indexCount][2] = ((participantList[indexCount][2] * 3) + exemplar[2]) / 4
        if score <= bottomQuarterScore:
            partcipantList[indexCount] = setParticipants(1)
        indexCount += 1
    return participantList

def simulateTourney(profile):
    participantList = setParticipants(100)
    participantLength = len(participantList)
    count = 0
    while count < 100:
        compStatsList = []
        for participant in participantList:
            compStats = [playGame(participant, [profile["aggression"], profile["aversion"]]), playGame(participant, [profile["aggression"], profile["aversion"]]), playGame(participant, [profile["aggression"], profile["aversion"]])]
            compStatsList.append(compStats)
        alterPool(participantList, compStatsList)
        count += 1
    compStatsList = []
    for participant in participantList:
        compStats = [playGame(participant, [profile["aggression"], profile["aversion"]]), playGame(participant, [profile["aggression"], profile["aversion"]]), playGame(participant, [profile["aggression"], profile["aversion"]])]
        compStatsList.append(compStats)
    scoreList = sumScores(compStatsList)
    return participant[scoreList.index(max(scoreList))]
    