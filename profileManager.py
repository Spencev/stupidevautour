import json

def loadProfiles():
    statsProfiles = open("profiles.txt", "r")
    profileList = json.load(statsProfiles)
    print("Profiles loaded.")
    return profileList

def genUsers(profileList):
    userList = []
    for profile in profileList["profileList"]:
        userList.append(profile["user"])
    print("Profile list generated")
    return userList

def newUser(userInput, profileList):
    duplicate = False
    for profile in profileList["profileList"]:
        if userInput == profile["user"]:
            print("Duplicate name, try again.")
            duplicate = True
    if not duplicate:
        profileList["profileList"].append({"user":userInput, "aversion":1, "aversionList":[], "aggression":1, "aggressionList":[], "deception":0.5, "wins": 0, "losses": 0, "ties":0})
        statsProfiles = open("profiles.txt", "w")
        statsProfiles.truncate(0)
        statsProfiles.seek(0)
        json.dump(profileList, statsProfiles)
        print("Profile: " + userInput + " added.")

def selectProfile(nameChosen, profileList):
    for profile in profileList["profileList"]:
        if nameChosen == profile["user"]:
            print("Profile: " + nameChosen + " selected.")
            return profile

def removeProfile(nameChosen, profileList):
    for profile in profileList["profileList"]:
        if nameChosen == profile["user"]:
            profileList["profileList"].remove(profile)
            print("Profile: " + nameChosen + " removed.")

def save(username, profileList, userProfile):
    for profile in profileList["profileList"]:
        if username == profile["user"]:
            profile = userProfile
            statsProfiles = open("profiles.txt", "w")
            statsProfiles.truncate(0)
            statsProfiles.seek(0)
            json.dump(profileList, statsProfiles)
            print("Profile: " + username + " saved.")