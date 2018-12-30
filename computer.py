def spencerChoice(compHand, bidCard):
    
    bidCard = bidCard["value"]
    
    if bidCard == 10:
        return 15
    
    if bidCard == 9:
        return 14
    
    if bidCard == 8:
        return 13
    
    if bidCard == 7:
        return 12
    
    if bidCard == 6:
        return 11
    
    if bidCard == 5:
        return 10
    
    if bidCard == -5:
        return 9
    
    if bidCard == 4:
        return 8
    
    if bidCard == -4:
        return 7
    
    if bidCard == 3:
        return 6
    
    if bidCard == -3:
        return 5
    
    if bidCard == 2:
        return 4
    
    if bidCard == -2:
        return 3
    
    if bidCard == 1:
        return 2
    
    if bidCard == -1:
        return 1