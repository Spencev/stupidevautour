from tkinter import *
from PIL import ImageTk, Image
import random

valueCardsPlayer = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
valueCardsComputer = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

bidCards = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

currentBid = 0
currentPlayerBid = 0

playerScore = 0
computerScore = 0

#--------------------------------------------------------------------------------------------

class Window1:

    def __init__(self, master):

        self.master = master
        master.title("Stupid Vulture")
        master.geometry("1080x720")

        self.intro = Label(master, text="\nWelcome to Stupid Vulture - The card game!\n")
        self.intro.pack()

        self.play = Button(self.master, text="Play against Dan's AI", command=self.load_dan)
        self.play.pack()
        
        self.playSpence = Button(self.master, text="Play against Spencer's AI", command=self.load_spence)
        self.playSpence.pack()

        self.close = Button(self.master, text="Close", command=master.destroy)
        self.close.pack()

    def load_dan(self):
        
        self.intro.destroy()
        self.play.destroy()
        self.playSpence.destroy()
        self.close.destroy()

        self.another = Window2(self.master)
    
    def load_spence(self):
        
        self.intro.destroy()
        self.play.destroy()
        self.playSpence.destroy()
        self.close.destroy()
        
        self.another = WindowSpencePick(self.master)
        
class WindowSpencePick:
    
    def __init__(self, master):
        import spencemain as manager
        
        self.master = master
        
        profileList = manager.intialize()
        userList = manager.profile.genUsers(profileList)
        
        for userIndex in range(len(userList)):
            self.userButton = Button(self.master, text=userList[userIndex], command= lambda userIndex=userIndex: self.load_user(userList[userIndex]))
            self.userButton.pack()
        
        self.createNew = Button(self.master, text="Create a new profile", command=self.createProfile)
        self.createNew.pack()
        
        self.mm = Button(self.master, text="Main Menu", command=self.load_spence_game)
        self.mm.pack()
        
    def wipe(self):
        buttonList = self.master.pack_slaves()
        for button in buttonList:
            button.destroy()
    
    def load_user(self, user):
        import spencemain as manager
        profileList = manager.intialize()
        profile = manager.profile.selectProfile(user, profileList)
        
        self.wipe()
        self.another = WindowGame(self.master, profile)
    
    def createProfile(self):
        self.wipe()
        self.another = createProfileWindow(self.master)
    
    def load_spence_game(self):
        self.wipe()
        self.another = Window1(self.master)

class createProfileWindow:
    
    def __init__(self, master):
        
        self.master = master
        
        self.infoTag = Label(master, text="\nPlease enter your name:")
        self.infoTag.pack()
        
        self.userInput = Entry(self.master)
        self.userInput.pack()
        
        self.createProfile = Button(master, text="Create profile", command=lambda: self.insertProfile(self.userInput.get()))
        self.createProfile.pack()
        
        self.cancelButton = Button(master, text="Cancel", command=lambda: self.backToProfile())
        self.cancelButton.pack()
    
    def insertProfile(self, userInput):
        import spencemain as manager
        
        profileList = manager.intialize()
        manager.profile.newUser(userInput, profileList)
        profile = manager.profile.selectProfile(userInput, profileList)
        
        self.another = WindowGame(self.master, profile)
    
    def backToProfile(self):
        
        buttonList = self.master.pack_slaves()
        for button in buttonList:
            button.destroy()
        
        self.another = WindowSpencePick(self.master)
    
class WindowGame():
    
    def __init__(self, master, profile):
        
        self.master = master
        print("game window created with " + str(profile))
        
        global valueCardsPlayer
        global bidCards
        global currentBid
        global currentPlayerBid
        global playerScore
        global computerScore

        self.master = master
        
        # If players have no cards left, the game is over.

        if (valueCardsPlayer == [] and valueCardsComputer == []):

            if (playerScore > computerScore):
                self.playerWinsLabel = Label(master, text="PLAYER WINS!")
                self.playerWinsLabel.pack()
            else:
                self.computerWinsLabel = Label(master, text="COMPUTER WINS!")
                self.computerWinsLabel.pack()

            self.endGame = Label(master, text="The game is over.")
            self.endGame.pack()

            self.mm = Button(self.master, text="Close", command=master.destroy)
            self.mm.pack()
            
        else:

            # Get current card to bid on.

            bidCards = random.sample( bidCards, len(bidCards))
            currentBid = random.choice(bidCards)

            self.bidLabel = Label(master, text="Current Bid Card: " + str(currentBid))
            self.bidLabel.pack()

            # Choose a card amount of bid on current card (currently random).
            for cardNumber in valueCardsPlayer:
                self.cardPickButton = Button(self.master, text=cardNumber, command= lambda cardNumber=cardNumber: self.playCard(master, cardNumber))
                self.cardPickButton.pack(side='left')

            # Current scores.
            self.playerScoreLabel = Label(master, text="Player's Score: " + str(playerScore))
            self.playerScoreLabel.pack()

            self.computerScoreLabel = Label(master, text="Computer's Score: " + str(computerScore))
            self.computerScoreLabel.pack()

            # Continue to computer's turn to bid.
            
            self.continueGame = Button(self.master, text="Continue", command=self.load_game)
            self.continueGame.pack()
    
    def wipeButtons(self):
        widgetList = self.master.pack_slaves()
        for widget in widgetList:
            if str(type(widget)) == "<class 'tkinter.Button'>":
                widget.destroy()
    
    def playCard(self, master, cardNumber):
        self.master = master
        global valueCardsComputer
        global valueCardsPlayer
        global bidCards
        global currentBid
        global playerScore
        global computerScore
        
        valueCardsPlayer.remove(cardNumber)
        
        valueCardsComputer = random.sample(valueCardsComputer, len(valueCardsComputer))
        computerChoice = random.choice(valueCardsComputer)
        
        self.computerChoiceLabel = Label(master, text="Computer played: " + str(computerChoice))
        self.computerChoiceLabel.pack()
        
        self.playerChoiceLabel = Label(master, text="You played: " + str(cardNumber))
        self.playerChoiceLabel.pack()
        
        if currentBid > 0:
            if cardNumber > computerChoice:
                playerScore += currentBid
            if cardNumber < computerChoice:
                computerScore += currentBid
        else:
            if cardNumber > computerChoice:
                computerScore += currentBid
            if cardNumber < computerChoice:
                playerScore += currentBid
        
        self.wipeButtons()
        
        bidCards = random.sample( bidCards, len(bidCards))
        currentBid = random.choice(bidCards)

        self.bidLabel = Label(master, text="Current Bid Card: " + str(currentBid))
        self.bidLabel.pack()
        
        self.playerScoreLabel.destroy()
        self.computerScoreLabel.destroy()
        
        self.playerScoreLabel = Label(master, text="\n\nPlayer's Score: " + str(playerScore))
        self.playerScoreLabel.pack()

        self.computerScoreLabel = Label(master, text="Computer's Score: " + str(computerScore))
        self.computerScoreLabel.pack()
        
        for numberCard in valueCardsPlayer:
            self.cardPickButton = Button(self.master, text=numberCard, command= lambda numberCard=numberCard: self.playCard(master, numberCard))
            self.cardPickButton.pack(side='left')

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

class Window2:

    def __init__(self, master):

        self.master = master

        self.difficulty = Label(master, text="\nPlease select a difficulty: \n")
        self.difficulty.pack()

        self.easy = Button(self.master, text="Easy", command=self.load_game)
        self.easy.pack()

        self.medium = Button(self.master, text="Medium", command=self.load_game)
        self.medium.pack()

        self.hard = Button(self.master, text="Hard", command=self.load_game)
        self.hard.pack()

        self.mm = Button(self.master, text="Main Menu", command=self.load_new)
        self.mm.pack()

    def load_game(self):

        self.difficulty.destroy()
        self.easy.destroy()
        self.medium.destroy()
        self.hard.destroy()
        self.mm.destroy()

        self.another = Game(self.master)

    def load_new(self):
        
        self.difficulty.destroy()
        self.easy.destroy()
        self.medium.destroy()
        self.hard.destroy()
        self.mm.destroy()

        self.another = Window1(self.master)

class Game:

    def __init__(self, master):

        global valueCardsPlayer
        global bidCards
        global currentBid
        global currentPlayerBid
        global playerScore
        global computerScore

        self.master = master

        image = Image.open("card.png")
        img = ImageTk.PhotoImage(image)
        
        self.label = Label(image = img)
        self.label.image = img
        self.label.pack()

        # If players have no cards left, the game is over.

        if (valueCardsPlayer == [] and valueCardsComputer == []):

            if (playerScore > computerScore):
                self.playerWinsLabel = Label(master, text="PLAYER WINS!")
                self.playerWinsLabel.pack()
            else:
                self.computerWinsLabel = Label(master, text="COMPUTER WINS!")
                self.computerWinsLabel.pack()

            self.endGame = Label(master, text="The game is over.")
            self.endGame.pack()

            self.mm = Button(self.master, text="Close", command=master.destroy)
            self.mm.pack()
            
        else:

            # Get current card to bid on.

            bidCards = random.sample( bidCards, len(bidCards))
            currentBid = random.choice(bidCards)

            self.bidLabel = Label(master, text="Current Bid Card: " + str(currentBid))
            self.bidLabel.pack()

            # Player's turn text.

            self.playerLabel = Label(master, text="\nPLAYER'S TURN")
            self.playerLabel.pack()

            # Choose a card amount of bid on current card (currently random).

            valueCardsPlayer = random.sample(valueCardsPlayer, len(valueCardsPlayer))
            currentValueCard = random.choice(valueCardsPlayer)

            self.listLabel = Label(master, text=str(valueCardsPlayer))
            self.listLabel.pack()

            self.valueCardsLabel = Label(master, text=str(currentValueCard))
            self.valueCardsLabel.pack()

            # Save the current card the player is bidding.

            currentPlayerBid = currentValueCard

            # Current scores.

            self.playerScoreLabel = Label(master, text="\n\nPlayer's Score: " + str(playerScore))
            self.playerScoreLabel.pack()

            self.computerScoreLabel = Label(master, text="Computer's Score: " + str(computerScore))
            self.computerScoreLabel.pack()

            # Remove the card used to bid.

            valueCardsPlayer.remove(currentValueCard)

            # Continue to computer's turn to bid.
            
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
