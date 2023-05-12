import os

#Find the players' folders
PLAYER_FOLDERS = os.listdir("./players/")
PLAYERS = []

for folder in PLAYER_FOLDERS:
  files = os.listdir("./players/" + folder)
  if "mainAI.py" in files: 
    PLAYERS.append("./players/" + folder + "/mainAI.py")

print(PLAYERS)