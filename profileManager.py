import json

def loadProfiles():
    statsProfiles = open("profiles.txt", "r")
    profileList = json.load(statsProfiles)
    print(profileList)
    return profileList

def genUsers(profileList):
    userList = []
    for profile in profileList["profileList"]:
        userList.append(profile["user"])
    return userList

def newUser(userInput, profileList):
    duplicate = False
    for profile in profileList["profileList"]:
        if userInput == profile["user"]:
            print("Duplicate name, try again.")
            duplicate = True
    if not duplicate:
        profileList["profileList"].append({"user":userInput, "aversion":0, "aversionList":[], "aggression":0, "aggressionList":[], "wins": 0, "losses": 0})
        statsProfiles = open("profiles.txt", "w")
        statsProfiles.truncate(0)
        statsProfiles.seek(0)
        json.dump(profileList, statsProfiles)
        print("User: " + userInput + " added successfully!")

def selectProfile(nameChosen, profileList):
    for profile in profileList["profileList"]:
        if nameChosen == profile["user"]:
            return profile

def removeProfile(nameChosen, profileList):
    for profile in profileList["profileList"]:
        if nameChosen == profile["user"]:
            profileList["profileList"].remove(profile)

def saveProfile(username, profileList, userProfile):
    for profile in profileList["profileList"]:
        if username == profile["user"]:
            profile = userProfile
            statsProfiles = open("profiles.txt", "w")
            statsProfiles.truncate(0)
            statsProfiles.seek(0)
            json.dump(profileList, statsProfiles)
            print("Profile saved.")