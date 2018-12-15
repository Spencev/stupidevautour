def generatePercents(playerHand, compHand):
    percentMatrix = []
    for compCard in compHand:
        winCount = 0
        tieCount = 0
        loseCount = 0
        for playerCard in playerHand:
            if compCard > playerCard:
                winCount+=1
            if compCard == playerCard:
                tieCount+=1
            if compCard < playerCard:
                loseCount+=1
        percentMatrix.append([round((winCount/15)*100, 2), round((tieCount/15)*100, 2), round((loseCount/15)*100, 2)])
    return percentMatrix

ex1 = generatePercents([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
print(ex1)

statsProfile = open("stats.txt", "r+")

def aversionUpdate(playerHand, playerPlayed, compHand, compPlayed, lastCard):
    
        
