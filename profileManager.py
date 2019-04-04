import json

def loadProfiles(): #loads all profiles into the application
    statsProfiles = open("profiles.txt", "r") #open up the text file
    profileList = json.load(statsProfiles) #load it in
    print("Profiles loaded.")
    return profileList

def genUsers(profileList): #returns a user list in order to print them onto the ui for the profile selection page
    userList = []
    for profile in profileList["profileList"]:
        userList.append(profile["user"])
    print("Profile list generated")
    return userList

def newUser(userInput, profileList): #creating a new profile to hold the attributes.
    duplicate = False
    for profile in profileList["profileList"]:
        if userInput == profile["user"]: #if duplicate
            print("Duplicate name, try again.")
            duplicate = True
    if not duplicate:
        profileList["profileList"].append({"user":userInput, "aversion":1, "aversionList":[], "aggression":1, "aggressionList":[], "deception":0.5, "deceptionList":[], "wins": 0, "losses": 0, "ties":0}) #add the profile
        statsProfiles = open("profiles.txt", "w")
        statsProfiles.truncate(0)
        statsProfiles.seek(0)
        json.dump(profileList, statsProfiles)
        print("Profile: " + userInput + " added.")

def selectProfile(nameChosen, profileList): #selects the profile in order to load in the player's attributes
    for profile in profileList["profileList"]:
        if nameChosen == profile["user"]:
            print("Profile: " + nameChosen + " selected.")
            return profile

def removeProfile(nameChosen, profileList): # this is code which didnt end up being used, but I left in here just in case I wanted to use later
    for profile in profileList["profileList"]:
        if nameChosen == profile["user"]:
            profileList["profileList"].remove(profile)
            print("Profile: " + nameChosen + " removed.")

def save(username, profileList, userProfile): #this is used to save the information gathered in the current game in order to maintain memory between games
    for profile in profileList["profileList"]:
        if username == profile["user"]:#finding correct profile
            profile = userProfile
            statsProfiles = open("profiles.txt", "w")
            statsProfiles.truncate(0)
            statsProfiles.seek(0)
            json.dump(profileList, statsProfiles)
            print("Profile: " + username + " saved.")