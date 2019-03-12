import random

def setParticipants(amount):
    participantList = []
    for participant in range(0, amount):
        participantList.append([random.random(), random.random()])
    return participantList

def playGame(participant1, participant2):
    hand1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    hand2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    middleDeck = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    while len(middleDeck) > 0:

def simulateTourney(profile):
    participantList = setParticipants(100)
    participantLength = len(participantList)
    for participant in participantList:
        if len(participantList) != participantLength:
            participantLength = len(participantList)
        else:
            break
    if len(participantList) != 1:
        
            