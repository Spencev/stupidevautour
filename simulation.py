import random
import spencemain as utility
import profileManager as profile
import numpy as np

def setParticipants(amount): #sets up the participants in the gene pool for the algorithm, returned as a list
    participantList = []
    for participant in range(0, amount):
        participantList.append([round(random.uniform(0, 2), 4), round(random.uniform(0, 1.5), 4), round(random.random(), 4)]) #[0] is aggression, [1] is aversion, [2] is deception
    return participantList

def playGame(participant1, participant2): #simulates a game between two participants
    hand1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] #data for the game
    hand2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    score1 = 0
    score2 = 0
    middleDeck = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    while len(middleDeck) > 0: #until game is over
        currentBid = random.choice(middleDeck) #pick bid card
        pick = utility.decide(hand1, hand2, participant1, currentBid, middleDeck) #participant1's decision
        hand1Choice = hand1[pick]
        pick = utility.decide(hand2, hand1, participant2, currentBid, middleDeck) #participant2's decision aka the player's attributes
        hand2Choice = hand2[pick]
        hand1.remove(hand1Choice) #remove the choices from the respective hands
        hand2.remove(hand2Choice)
        middleDeck.remove(currentBid)
        if currentBid > 0: 
            if hand1Choice > hand2Choice: #1 wins the card
                score1 += currentBid
            elif hand2Choice > hand1Choice: #2 wins the card
                score2 += currentBid
            else: #tie
                continue
        if currentBid < 0: 
            if hand1Choice > hand2Choice: #1 wins the card
                score2 += currentBid
            elif hand2Choice > hand1Choice: #2 wins the card
                score1 += currentBid
            else: #tie
                continue
    if score1 > score2: #1 wins the game
        return [1, score1 - score2]
    elif score1 < score2: #2 wins the game
        return [-1, score1 - score2]
    else: #tie
        return [0, 0]

def sumScores(compStatsList): #create the value of the fitness for the agent details of the way this is derived is in the report
    scoreList = []
    for stat in compStatsList:
        score = 0
        for game in stat:
            score += (game[0] * 30) + game[1]
        scoreList.append(score)
    return scoreList

def alterPool(participantList, compStatsList): #change the gene pool through rerolling bottom quartile and crossing over with 2nd and 4th quartile
    scoreList = sumScores(compStatsList) #gets the fitness for all participants
    medianScore = np.percentile(scoreList, 50)
    bottomQuarterScore = np.percentile(scoreList, 25)
    topQuarterScore = np.percentile(scoreList, 75)
    indexCount = 0
    topOfPool = []
    for score in scoreList: #sorts out the top of the pool for the exemplars
        if score >= topQuarterScore:
            topOfPool.append(participantList[indexCount])
        indexCount += 1
    indexCount = 0
    for score in scoreList: #iterate through for the participants which will be changed
        if score > medianScore: #50-75 range is untouched
            continue
        if score <= medianScore and score > bottomQuarterScore: #second quartile which gets crossed over
            exemplar = random.choice(topOfPool) #pick the exemplar
            participantList[indexCount][0] = ((participantList[indexCount][0] * 3) + exemplar[0]) / 4 #cross over all attributes
            participantList[indexCount][1] = ((participantList[indexCount][1] * 3) + exemplar[1]) / 4
            participantList[indexCount][2] = ((participantList[indexCount][2] * 3) + exemplar[2]) / 4
        if score <= bottomQuarterScore: #bottom quartile gets rerolled completely
            participantList[indexCount] = (setParticipants(1))[0]
        indexCount += 1
    return participantList

def simulateTourney(profile): #runs the genetic algorithm
    participantList = setParticipants(50) #50 participants in the pool
    aggression = profile["aggression"] #getting the player's attributes
    aversion = profile["aversion"]
    deception = profile["deception"]
    count = 0
    while count < 50: #number of iterations of training 
        print(count) #keeping this here to monitor progress while loading 
        compStatsList = []
        for participant in participantList:
            compStatsList.append([playGame(participant, [aggression, aversion, deception]), playGame(participant, [aggression, aversion, deception]), playGame(participant, [aggression, aversion, deception])])#play 3 games
        alterPool(participantList, compStatsList) #alter the pool
        count += 1
    compStatsList = []
    for participant in participantList: #collect final fitness values
        compStatsList.append([playGame(participant, [aggression, aversion, deception]), playGame(participant, [aggression, aversion, deception]), playGame(participant, [aggression, aversion, deception])])
    scoreList = sumScores(compStatsList)
    return participantList[scoreList.index(max(scoreList))] #pick the best one