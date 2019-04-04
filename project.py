from tkinter import *
from PIL import ImageTk, Image
import random
import spencemain as manager
import simulation as sim

#Game engine code written by Spencer Delaney and Daniel Hughes (this file)
#Rest of the code written by Spencer Delaney

#The comments don't go into a huge amount of detail for the GUI but go more in depth for stuff that matters more
#Further explanation provided in the pdf included in this folder

#used global variables which, despite their stigma, are not that bad to work with with proper organization
valueCardsPlayer = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] 
valueCardsComputer = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

bidCards = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

currentBid = 0
currentPlayerBid = 0

playerScore = 0
computerScore = 0

profileList = manager.initialize() #loading profile list

class Window1:

    def __init__(self, master):
        
        self.master = master #configuration for the ui on the launch screen
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
    
    def load_spence(self, master): #load the next window after hittin play
        
        self.intro.destroy() #clean up the window
        self.playSpence.destroy()
        self.close.destroy()
        master.grid_rowconfigure(5, weight=0)
        
        self.another = WindowSpencePick(self.master) #move to next window
        
class WindowSpencePick: #window which has profile selection
    
    def __init__(self, master):
        global profileList
        
        self.master = master
        
        self.infoText = Label(master, text="Please select a profile") #title label
        self.infoText.configure(background="#034D01")
        self.infoText.configure(foreground="white")
        self.infoText.grid(row=1, column=1, sticky=NSEW)
        
        userList = manager.profile.genUsers(profileList)
        
        rowTracker = 2 #track which row we are on for the grid system used
        
        for userIndex in range(len(userList)): #iterate through the profiles to create the buttons to select them
            self.userButton = Button(self.master, text=userList[userIndex], command= lambda userIndex=userIndex: self.load_user(userList[userIndex]))
            self.userButton.grid(row=rowTracker, column=1, pady=(10, 0), sticky=NSEW)
            rowTracker += 1
        
        self.createNew = Button(self.master, text="Create a new profile", command=self.createProfile) #create a new profile instead
        self.createNew.grid(row=rowTracker, column=1, pady=(20, 0), sticky=NSEW)
        rowTracker += 1
        
        self.checkStats = Button(self.master, text="Check all stats", command=self.checkStatistics) #check stats for all users
        self.checkStats.grid(row=rowTracker, column=1, pady=(20, 0), sticky=NSEW)
        rowTracker += 1
        
        self.mm = Button(self.master, text="Main Menu", command=self.load_spence_game) #back to main menu
        self.mm.grid(row=rowTracker, column=1, pady=(10, 0), sticky=NSEW)
        rowTracker += 1
        
        master.grid_rowconfigure(rowTracker, weight=1)

    def wipe(self): #destroy all the profile buttons
        buttonList = self.master.grid_slaves()
        for button in buttonList:
            button.destroy()
    
    def load_user(self, user): #import the user
        import spencemain as manager
        profile = manager.profile.selectProfile(user, profileList)
        
        self.wipe()
        self.another = WindowGame(self.master, profile)
    
    def createProfile(self): #move to create profile window
        self.wipe()
        self.another = createProfileWindow(self.master)
    
    def checkStatistics(self): #move to checking stats profile
        self.wipe()
        self.another = statsWindow(self.master)
    
    def load_spence_game(self): #back to main menu
        self.wipe()
        self.another = Window1(self.master)
        
class statsWindow: #window for profile statistics
    def __init__(self, master):
        global profileList
        
        self.master = master
        
        self.infoTag = Label(master, text="\nStats for all profiles") #title text
        self.infoTag.configure(background="#034D01")
        self.infoTag.configure(foreground="white")
        self.infoTag.grid(row=1, column=1, sticky=NSEW)
        
        compWins = 0
        compLosses = 0
        compTies = 0
        rowTracker = 2
        
        for profile in profileList["profileList"]: #iterating through all of the profile
            compWins += profile["losses"]
            compLosses += profile["wins"]
            compTies += profile["ties"]
            self.userLabel = Label(self.master, text=profile["user"] + ": Wins: " + str(profile["wins"]) + " Losses: " + str(profile["losses"]) + " Ties: " + str(profile["ties"]))
            self.userLabel.configure(background="#034D01")
            self.userLabel.configure(foreground="white")
            self.userLabel.grid(row=rowTracker, column=1, pady=(10, 0), sticky=NSEW)
            rowTracker += 1
        
        self.compLabel = Label(self.master, text="Computer: Wins: " + str(compWins) + " Losses: " + str(compLosses) + " Ties: " + str(compTies) + "\n") #adds the computer's stats
        self.compLabel.configure(background="#034D01")
        self.compLabel.configure(foreground="white")
        self.compLabel.grid(row=rowTracker, column=1, pady=(10, 0), sticky=NSEW)
        rowTracker += 1
        
        self.backButton = Button(master, text="Back to profile select", command=self.backToMenu) #back to profile selection
        self.backButton.grid(row=rowTracker, column=1, pady=(10, 0), sticky=NSEW)
    
    def wipe(self): #clear page
        buttonList = self.master.grid_slaves()
        for button in buttonList:
            button.destroy()
        
    def backToMenu(self): #go back to menu
        self.wipe()
        self.backButton.destroy()
        self.another = WindowSpencePick(self.master)

class createProfileWindow: #window for creating a profile
    
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
    
    def insertProfile(self, userInput): #add the profile to the list
        import spencemain as manager
        
        manager.profile.newUser(userInput, profileList)
        profile = manager.profile.selectProfile(userInput, profileList)
        
        widgetList = self.master.grid_slaves()
        for widget in widgetList:
            widget.destroy()
        
        self.another = WindowGame(self.master, profile)
    
    def backToProfile(self): #back to previous screen
        
        buttonList = self.master.grid_slaves()
        for button in buttonList:
            button.destroy()
        
        self.another = WindowSpencePick(self.master)
    
class WindowGame(): #window for actual game
    
    def __init__(self, master, profile):
        
        self.master = master
        print("Game window created for " + profile["user"] + ".")
        
        global compAttributes
        compAttributes = sim.simulateTourney(profile) #simulates the tournament to find the best agent 
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
        
        #data for the running of the game
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
        
        #show the image of the card on screen
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

    def backToMenu(self, master): #quit the game
        widgetList = self.master.grid_slaves() + self.master.place_slaves()
        for widget in widgetList:
            widget.destroy()
        
        self.backButton.destroy()
        
        self.another = WindowSpencePick(self.master)
        
    def wipeButtons(self, playersHand, history):
        widgetList = self.master.grid_slaves() + self.master.pack_slaves()
        for widget in widgetList:
            widget.destroy()
    
    def playCard(self, master, cardNumber, profile, playersHand, history): #triggered when the player plays a card 
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
        
        if currentBid["value"] == bidDict[-1]["value"]: #checking to see if the player did a deception
            manager.updateDeception(playersHand, cardNumber, valueCardsComputer, currentBid["value"], profile) #this is accomplished in here
            
            if currentBid["value"] > 0:
                posMiddleDeck = []
                for card in bidDict:
                    if card["value"] > 0:
                        posMiddleDeck.append(card["value"])
                manager.updateAggression(playersHand, cardNumber, currentBid["value"], posMiddleDeck, profile) #update the players aggression
            
            computerChoice = valueCardsComputer[manager.decide(valueCardsPlayer, valueCardsComputer, compAttributes, currentBid["value"], bidCards)] #get the computers choice on this bid
            valueCardsComputer.remove(computerChoice)
            
            if cardNumber > computerChoice: #adding scores
                playerScore += currentBid["value"]
            if cardNumber < computerChoice:
                computerScore += currentBid["value"]
        
        elif currentBid["value"] > 0: #aggression checking 
            posMiddleDeck = []
            for card in bidDict:
                if card["value"] > 0:
                    posMiddleDeck.append(card["value"])
            manager.updateAggression(playersHand, cardNumber, currentBid["value"], posMiddleDeck, profile) #update the players aggression
            
            computerChoice = valueCardsComputer[manager.decide(valueCardsPlayer, valueCardsComputer, compAttributes, currentBid["value"], bidCards)] #get the computers choice on this bid
            valueCardsComputer.remove(computerChoice)
            
            if cardNumber > computerChoice: #adding scores
                playerScore += currentBid["value"]
            if cardNumber < computerChoice:
                computerScore += currentBid["value"]
                
        else:
            negMiddleDeck = []
            for card in bidDict:
                if card["value"] < 0:
                    negMiddleDeck.append(card["value"])
            manager.updateAversion(playersHand, cardNumber, currentBid["value"], negMiddleDeck, profile) #update the players aversion
            
            computerChoice = valueCardsComputer[manager.decide(valueCardsPlayer, valueCardsComputer, compAttributes, currentBid["value"], bidCards)] #get the computers choice on this bid
            valueCardsComputer.remove(computerChoice)
            
            if cardNumber > computerChoice: #adding scores
                computerScore += currentBid["value"]
            if cardNumber < computerChoice:
                playerScore += currentBid["value"]
        
        valueCardsPlayer.remove(cardNumber) #remove the cards played from the list
        bidDict.remove(currentBid)
        
        self.wipeButtons(playersHand, history)
        self.bidLabel.destroy()
        self.playerScoreLabel.destroy()
        self.computerScoreLabel.destroy()
        self.playerChoiceLabel = Label(history, text="")
        self.computerChoiceLabel = Label(history, text="")
        self.playerChoiceLabel.destroy()
        self.computerChoiceLabel.destroy()
        
        if bidDict != []: #go to next card
            
            currentBid = random.choice(bidDict)
            
            playersHand = Frame(master)
            playersHand.grid(row=3, column=1)

            image = Image.open(currentBid["image"])
            img = ImageTk.PhotoImage(image)

            self.bidLabel = Label(image = img)
            self.bidLabel.image = img
            self.bidLabel.configure(background="#034D01")
            self.bidLabel.grid(row=2, column=1)
        
        else: #game is over
            
            if (playerScore > computerScore): #player wins
                self.playerWinsLabel = Label(master, text="You win!")
                self.playerWinsLabel.configure(foreground="white")
                self.playerWinsLabel.configure(background="#034D01")
                self.playerWinsLabel.grid(row=3, column=1)
                profile["wins"] += 1
                
            elif (playerScore < computerScore): #comp wins
                self.computerWinsLabel = Label(master, text="Computer wins!")
                self.computerWinsLabel.configure(foreground="white")
                self.computerWinsLabel.configure(background="#034D01")
                self.computerWinsLabel.grid(row=3, column=1)
                profile["losses"] += 1
                
            else: #tie
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
        
        for numberCard in valueCardsPlayer: #creating the buttons for the player to select the cards
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

    def goAgain(self, master, profile): #play again
        
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
        
def main():
    root = Tk()
    run = Window1(root)
    root.mainloop()

main()
