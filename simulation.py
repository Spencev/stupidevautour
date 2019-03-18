import random
import spencemain as utility
import profileManager as profile

def setParticipants(amount):
    participantList = []
    for participant in range(0, amount):
        participantList.append([random.random(), random.random()])
    return participantList

def playGame(participant1, participant2):
    hand1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    hand2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    score1 = 0
    score2 = 0
    middleDeck = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    while len(middleDeck) > 0:
        currentBid = random.choice(middleDeck)
        middleDeck.remove(currentBid)
        percentMatrix = utility.generatePercents(hand1, hand2)
        hand1Choice = random.choice(hand1)
        hand1.remove(hand1Choice)
        hand2Choice = random.choice(hand2)
        hand2.remove(hand2Choice)
        #print("bid: " + str(currentBid))
        #print("comp: " + str(hand1Choice))
        #print("player: " + str(hand2Choice))
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
        #print("player score: " + str(score2))
        #print("comp score: " + str(score1))
    if score1 > score2:
        return [1, score1 - score2]
    elif score1 < score2:
        return [-1, score1 - score2]
    else:
        return [0, 0]

def simulateTourney(profile):
    participantList = setParticipants(100)
    participantLength = len(participantList)
    count = 0
    cuttingDown = True
    while cuttingDown and count < 100:
        if len(participantList) == 1:
            break
        for participant in participantList:
            compStats = [playGame(participant, [profile["aggression"], profile["aversion"]]), playGame(participant, [profile["aggression"], profile["aversion"]]), playGame(participant, [profile["aggression"], profile["aversion"]])]
            if (compStats[0][0] + compWin[1][0] + compStats[2][0]) <= 0:
                participant = setParticipants(1)
        if len(participantList) != participantLength:
            participantLength = len(participantList)
        else:
            cuttingDown = False
        print(participantList)
    print(participantList)
    
profileList = profile.loadProfiles()
spenceProfile = profile.selectProfile("Spencer", profileList)
simulateTourney(spenceProfile)
print(playGame([1, 1], [1, 1]))