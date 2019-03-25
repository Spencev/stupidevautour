from tkinter import *
from PIL import ImageTk, Image
import random
import spencemain as manager
import simulation as sim

valueCardsPlayer = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
valueCardsComputer = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

bidCards = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

currentBid = 0
currentPlayerBid = 0

playerScore = 0
computerScore = 0

profileList = manager.initialize()

class Window1:

    def __init__(self, master):
        
        self.master = master
        master.title("Stupid Vulture")
        master.geometry("1080x720")
        master.configure(background="#034D01")
        master.grid_rowconfigure(0, weight=1)
        master.grid_rowconfigure(5, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(2, weight=1)
        
        self.intro = Label(master, text="\nWelcome to Stupid Vulture - The card game!\n")
        self.intro.configure(background="#034D01")
        self.intro.configure(foreground="white")
        self.intro.grid(row=1, column=1, sticky=NSEW)
        
        self.playSpence = Button(self.master, text="Play", command=lambda:self.load_spence(master))
        self.playSpence.grid(row=2, column=1, pady=(0, 0))

        self.close = Button(self.master, text="Close", command=master.destroy)
        self.close.grid(row=3, column=1, pady=(10, 0))
    
    def load_spence(self, master):
        
        self.intro.destroy()
        self.playSpence.destroy()
        self.close.destroy()
        master.grid_rowconfigure(5, weight=0)
        
        self.another = WindowSpencePick(self.master)
        
class WindowSpencePick:
    
    def __init__(self, master):
        global profileList
        
        self.master = master
        
        self.infoText = Label(master, text="Please select a profile")
        self.infoText.configure(background="#034D01")
        self.infoText.configure(foreground="white")
        self.infoText.grid(row=1, column=1, sticky=NSEW)
        
        userList = manager.profile.genUsers(profileList)
        
        rowTracker = 2
        
        for userIndex in range(len(userList)):
            self.userButton = Button(self.master, text=userList[userIndex], command= lambda userIndex=userIndex: self.load_user(userList[userIndex]))
            self.userButton.grid(row=rowTracker, column=1, pady=(10, 0), sticky=NSEW)
            rowTracker += 1
        
        self.createNew = Button(self.master, text="Create a new profile", command=self.createProfile)
        self.createNew.grid(row=rowTracker, column=1, pady=(20, 0), sticky=NSEW)
        rowTracker += 1
        
        self.checkStats = Button(self.master, text="Check all stats", command=self.checkStatistics)
        self.checkStats.grid(row=rowTracker, column=1, pady=(20, 0), sticky=NSEW)
        rowTracker += 1
        
        self.mm = Button(self.master, text="Main Menu", command=self.load_spence_game)
        self.mm.grid(row=rowTracker, column=1, pady=(10, 0), sticky=NSEW)
        rowTracker += 1
        
        master.grid_rowconfigure(rowTracker, weight=1)

    def wipe(self):
        buttonList = self.master.grid_slaves()
        for button in buttonList:
            button.destroy()
    
    def load_user(self, user):
        import spencemain as manager
        profile = manager.profile.selectProfile(user, profileList)
        
        self.wipe()
        self.another = WindowGame(self.master, profile)
    
    def createProfile(self):
        self.wipe()
        self.another = createProfileWindow(self.master)
    
    def checkStatistics(self):
        self.wipe()
        self.another = statsWindow(self.master)
    
    def load_spence_game(self):
        self.wipe()
        self.another = Window1(self.master)
        
class statsWindow:
    def __init__(self, master):
        global profileList
        
        self.master = master
        
        self.infoTag = Label(master, text="\nStats for all profiles")
        self.infoTag.configure(background="#034D01")
        self.infoTag.configure(foreground="white")
        self.infoTag.grid(row=1, column=1, sticky=NSEW)
        
        compWins = 0
        compLosses = 0
        compTies = 0
        rowTracker = 2
        
        for profile in profileList["profileList"]:
            compWins += profile["losses"]
            compLosses += profile["wins"]
            compTies += profile["ties"]
            self.userLabel = Label(self.master, text=profile["user"] + ": Wins: " + str(profile["wins"]) + " Losses: " + str(profile["losses"]) + " Ties: " + str(profile["ties"]))
            self.userLabel.configure(background="#034D01")
            self.userLabel.configure(foreground="white")
            self.userLabel.grid(row=rowTracker, column=1, pady=(10, 0), sticky=NSEW)
            rowTracker += 1
        
        self.compLabel = Label(self.master, text="Computer: Wins: " + str(compWins) + " Losses: " + str(compLosses) + " Ties: " + str(compTies) + "\n")
        self.compLabel.configure(background="#034D01")
        self.compLabel.configure(foreground="white")
        self.compLabel.grid(row=rowTracker, column=1, pady=(10, 0), sticky=NSEW)
        rowTracker += 1
        
        self.backButton = Button(master, text="Back to profile select", command=self.backToMenu)
        self.backButton.grid(row=rowTracker, column=1, pady=(10, 0), sticky=NSEW)
    
    def wipe(self):
        buttonList = self.master.grid_slaves()
        for button in buttonList:
            button.destroy()
        
    def backToMenu(self):
        self.wipe()
        self.backButton.destroy()
        self.another = WindowSpencePick(self.master)

class createProfileWindow:
    
    def __init__(self, master):
        
        self.master = master
        
        self.infoTag = Label(master, text="Please enter your name:")
        self.infoTag.configure(background="#034D01")
        self.infoTag.configure(foreground="white")
        self.infoTag.grid(row=1, column=1, sticky=NSEW)
        
        self.userInput = Entry(self.master)
        self.userInput.grid(row=2, column=1, pady=(10, 0), sticky=NSEW)
        
        self.createProfile = Button(master, text="Create profile", command=lambda: self.insertProfile(self.userInput.get()))
        self.createProfile.grid(row=3, column=1, pady=(20, 0), sticky=NSEW)
        
        self.cancelButton = Button(master, text="Cancel", command=lambda: self.backToProfile())
        self.cancelButton.grid(row=4, column=1, pady=(10, 0), sticky=NSEW)
    
    def insertProfile(self, userInput):
        import spencemain as manager
        
        manager.profile.newUser(userInput, profileList)
        profile = manager.profile.selectProfile(userInput, profileList)
        
        widgetList = self.master.grid_slaves()
        for widget in widgetList:
            widget.destroy()
        
        self.another = WindowGame(self.master, profile)
    
    def backToProfile(self):
        
        buttonList = self.master.grid_slaves()
        for button in buttonList:
            button.destroy()
        
        self.another = WindowSpencePick(self.master)
    
class WindowGame():
    
    def __init__(self, master, profile):
        
        self.master = master
        print("Game window created for " + profile["user"] + ".")
        
        global compAttributes
        compAttributes = sim.simulateTourney(profile)
        print("Tournament completed. " + str(compAttributes) + " is the winner!")
        
        global valueCardsPlayer
        global valueCardsComputer
        global bidCards
        global bidDict
        global currentBid
        global currentPlayerBid
        global playerScore
        global computerScore

        self.master = master
        
        valueCardsPlayer = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        valueCardsComputer = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        
        bidDict = [{"value": -5, "image":"imgs/card-5.png"}, 
                   {"value": -4, "image":"imgs/card-4.png"}, 
                   {"value": -3, "image":"imgs/card-3.png"}, 
                   {"value": -2, "image":"imgs/card-2.png"}, 
                   {"value": -1, "image":"imgs/card-1.png"},
                   {"value": 1, "image":"imgs/card1.png"}, 
                   {"value": 2, "image":"imgs/card2.png"},
                   {"value": 3, "image":"imgs/card3.png"},
                   {"value": 4, "image":"imgs/card4.png"},
                   {"value": 5, "image":"imgs/card5.png"},
                   {"value": 6, "image":"imgs/card6.png"},
                   {"value": 7, "image":"imgs/card7.png"},
                   {"value": 8, "image":"imgs/card8.png"},
                   {"value": 9, "image":"imgs/card9.png"},
                   {"value": 10, "image":"imgs/card10.png"}]

        currentBid = 0
        currentPlayerBid = 0

        playerScore = 0
        computerScore = 0
        
        # Get current card to bid on.
        currentBid = random.choice(bidDict)
        

        image = Image.open(currentBid["image"])
        img = ImageTk.PhotoImage(image)
        
        history = Frame(master)
        history.configure(background="#034D01")
        history.place(relx=1, x=-10, y=40, anchor=NE)
        
        playersHand = Frame(master)
        playersHand.grid(row=3, column=1)
        
        columnTracker = 0
        
        # Choose a card amount of bid on current card (currently random).
        for cardNumber in valueCardsPlayer:
            self.cardPickButton = Button(playersHand, text=cardNumber, command= lambda cardNumber=cardNumber: self.playCard(master, cardNumber, profile, valueCardsPlayer, history))
            self.cardPickButton.grid(row=6, column=columnTracker)
            columnTracker += 1
            
        self.bidLabel = Label(image = img)
        self.bidLabel.image = img
        self.bidLabel.configure(background="#034D01")
        self.bidLabel.grid(row=2, column=1)

        # Current scores.
        self.playerScoreLabel = Label(master, text="Your Score: " + str(playerScore))
        self.playerScoreLabel.configure(foreground="white")
        self.playerScoreLabel.configure(background="#034D01")
        self.playerScoreLabel.grid(row=4, column=1)

        self.computerScoreLabel = Label(master, text="Computer's Score: " + str(computerScore))
        self.computerScoreLabel.configure(foreground="white")
        self.computerScoreLabel.configure(background="#034D01")
        self.computerScoreLabel.grid(row=5, column=1)
        
        self.backButton = Button(self.master, text="Back to menu", command= lambda: self.backToMenu(master))
        self.backButton.place(relx=1, x=-10, y=40, anchor=SE)

    def backToMenu(self, master):
        widgetList = self.master.grid_slaves() + self.master.place_slaves()
        for widget in widgetList:
            widget.destroy()
        
        self.backButton.destroy()
        
        self.another = WindowSpencePick(self.master)
        
    def wipeButtons(self, playersHand, history):
        widgetList = self.master.grid_slaves() + self.master.pack_slaves()
        for widget in widgetList:
            widget.destroy()
    
    def playCard(self, master, cardNumber, profile, playersHand, history):
        import spencemain as manager
        
        self.master = master
        global valueCardsComputer
        global valueCardsPlayer
        global bidCards
        global bidDict
        global currentBid
        global playerScore
        global computerScore
        global profileList
        global compAttributes
        
        computerChoice = valueCardsComputer[manager.decide(valueCardsPlayer, valueCardsComputer, compAttributes, currentBid["value"], bidCards)-1]
        print(computerChoice)
        print(valueCardsComputer)
        valueCardsComputer.remove(computerChoice)
        
        if currentBid["value"] > 0:
            posMiddleDeck = []
            for card in bidDict:
                if card["value"] > 0:
                    posMiddleDeck.append(card["value"])
            print(posMiddleDeck)
            manager.updateAggression(playersHand, cardNumber, currentBid["value"], posMiddleDeck, profile)
            
            if cardNumber > computerChoice:
                playerScore += currentBid["value"]
            if cardNumber < computerChoice:
                computerScore += currentBid["value"]
                
        else:
            negMiddleDeck = []
            for card in bidDict:
                if card["value"] < 0:
                    negMiddleDeck.append(card["value"])
            manager.updateAversion(playersHand, cardNumber, currentBid["value"], negMiddleDeck, profile)
            
            if cardNumber > computerChoice:
                computerScore += currentBid["value"]
            if cardNumber < computerChoice:
                playerScore += currentBid["value"]
        
        valueCardsPlayer.remove(cardNumber)
        bidDict.remove(currentBid)
        
        self.wipeButtons(playersHand, history)
        self.bidLabel.destroy()
        self.playerScoreLabel.destroy()
        self.computerScoreLabel.destroy()
        self.playerChoiceLabel = Label(history, text="")
        self.computerChoiceLabel = Label(history, text="")
        self.playerChoiceLabel.destroy()
        self.computerChoiceLabel.destroy()
        
        if bidDict != []:
            
            currentBid = random.choice(bidDict)
            
            playersHand = Frame(master)
            playersHand.grid(row=3, column=1)

            image = Image.open(currentBid["image"])
            img = ImageTk.PhotoImage(image)

            self.bidLabel = Label(image = img)
            self.bidLabel.image = img
            self.bidLabel.configure(background="#034D01")
            self.bidLabel.grid(row=2, column=1)
        
        else:
            
            if (playerScore > computerScore):
                self.playerWinsLabel = Label(master, text="You win!")
                self.playerWinsLabel.configure(foreground="white")
                self.playerWinsLabel.configure(background="#034D01")
                self.playerWinsLabel.grid(row=3, column=1)
                profile["wins"] += 1
                
            elif (playerScore < computerScore):
                self.computerWinsLabel = Label(master, text="Computer wins!")
                self.computerWinsLabel.configure(foreground="white")
                self.computerWinsLabel.configure(background="#034D01")
                self.computerWinsLabel.grid(row=3, column=1)
                profile["losses"] += 1
                
            else:
                self.tiedLabel = Label(master, text="You tied!")
                self.tiedLabel.configure(foreground="white")
                self.tiedLabel.configure(background="#034D01")
                self.tiedLabel.grid(row=3, column=1)
                profile["ties"] += 1
            
            manager.profile.save(profile["user"], profileList, profile)
            
            self.backButton.destroy()
            
            self.playAgain = Button(self.master, text="Play Again", command= lambda: self.goAgain(master, profile))
            self.playAgain.grid(row=6, column=1, pady=(10,0))
            
            self.mainMenu = Button(self.master, text="Back to Menu", command= lambda: self.backToMenu(master))
            self.mainMenu.grid(row=7, column=1, pady=(10,0))

            self.closeGame = Button(self.master, text="Exit Game", command=master.destroy)
            self.closeGame.grid(row=8, column=1, pady=(10,0))
        
        for numberCard in valueCardsPlayer:
            self.cardPickButton = Button(playersHand, text=numberCard, command= lambda numberCard=numberCard: self.playCard(master, numberCard, profile, valueCardsPlayer, history))
            self.cardPickButton.pack(side='left')
        
        self.playerScoreLabel = Label(master, text="Your Score: " + str(playerScore))
        self.playerScoreLabel.configure(foreground="white")
        self.playerScoreLabel.configure(background="#034D01")
        self.playerScoreLabel.grid(row=4, column=1)

        self.computerScoreLabel = Label(master, text="Computer's Score: " + str(computerScore))
        self.computerScoreLabel.configure(foreground="white")
        self.computerScoreLabel.configure(background="#034D01")
        self.computerScoreLabel.grid(row=5, column=1)
        
        self.computerChoiceLabel = Label(history, text="Computer played: " + str(computerChoice))
        self.computerChoiceLabel.configure(foreground="white")
        self.computerChoiceLabel.configure(background="#034D01")
        self.computerChoiceLabel.pack()
        
        self.playerChoiceLabel = Label(history, text="You played: " + str(cardNumber))
        self.playerChoiceLabel.configure(foreground="white")
        self.playerChoiceLabel.configure(background="#034D01")
        self.playerChoiceLabel.pack()

    def goAgain(self, master, profile):
        
        widgetList = self.master.grid_slaves() + self.master.place_slaves()
        for widget in widgetList:
            widget.destroy()
        
        self.backButton.destroy()
        
        self.another = WindowGame(self.master, profile)
        
    def load_game(self):

        self.valueCardsLabel.destroy()
        self.continueGame.destroy()
        self.label.destroy()
        self.listLabel.destroy()
        self.playerLabel.destroy()
        self.bidLabel.destroy()
        self.playerScoreLabel.destroy()
        self.computerScoreLabel.destroy()
        
        self.another = Computer(self.master)        

    def load_new(self):

        self.endGame.destroy()
        self.mm.destroy()
        self.label.destroy()
        self.playerWinsLabel.destroy()
        self.computerWinsLabel.destroy()

        self.another = Window1(self.master)

class Computer:
    
    def __init__(self, master):

        global valueCardsComputer
        global computerScore
        global playerScore
        global bidCards
        global currentBid
        global currentPlayerBid

        self.master = master

        image = Image.open("card.png")
        img = ImageTk.PhotoImage(image)
        
        self.label = Label(image = img)
        self.label.image = img
        self.label.pack()

        # If players have no cards left, the game is over.

        if (valueCardsComputer == [] and valueCardsPlayer == []):

            self.endGame = Label(master, text="The game is over.")
            self.endGame.pack()

            self.mm = Button(self.master, text="Close", command=master.destroy)
            self.mm.pack()
            
        else:

            # Restate current card to bid on.

            self.bidLabel = Label(master, text="Current Bid Card: " + str(currentBid))
            self.bidLabel.pack()

            # Player's turn text.

            self.playerLabel = Label(master, text="\nCOMPUTER'S TURN")
            self.playerLabel.pack()

            # Choose a card amount of bid on current card (currently random).

            valueCardsComputer = random.sample(valueCardsComputer, len(valueCardsComputer))
            currentValueCard = random.choice(valueCardsComputer)

            self.listLabel = Label(master, text=str(valueCardsComputer))
            self.listLabel.pack()

            self.valueCardsLabel = Label(master, text=str(currentValueCard))
            self.valueCardsLabel.pack()

            # See if player or computer wins the card.

            playerDist = abs(currentBid - currentPlayerBid)
            compDist = abs(currentBid- currentValueCard)

            if (playerDist < compDist):
                playerScore = playerScore + currentBid
            else:
                computerScore = computerScore + currentBid

            self.playerScoreLabel = Label(master, text="\n\nPlayer's Score: " + str(playerScore))
            self.playerScoreLabel.pack()

            self.computerScoreLabel = Label(master, text="Computer's Score: " + str(computerScore))
            self.computerScoreLabel.pack()

            # Remove the card used to bid AND remove bid card to continue the game.

            valueCardsComputer.remove(currentValueCard)
            bidCards.remove(currentBid)

            # Continue back to player. 1 round has been completed.
            
            self.continueGame = Button(self.master, text="Continue", command=self.load_game)
            self.continueGame.pack()

    def load_game(self):

        self.valueCardsLabel.destroy()
        self.continueGame.destroy()
        self.label.destroy()
        self.listLabel.destroy()
        self.playerLabel.destroy()
        self.bidLabel.destroy()
        self.playerScoreLabel.destroy()
        self.computerScoreLabel.destroy()
              
        self.another = Game(self.master)

    def load_new(self):

        self.endGame.destroy()
        self.mm.destroy()
        self.label.destroy()

        self.another = Window1(self.master)
        
def main():
    root = Tk()
    run = Window1(root)
    root.mainloop()

main()
