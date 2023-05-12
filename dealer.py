import random
import sys
import os
import subprocess
import datetime
# RULES OF HEARTS
# 1. The simulated version of hearts in this file is the 4 player variant. Each player is dealt 13 cards
# 2. A game is over when a player reaches 100 points at the end of a round.
#    If multiple players go over 100, the player with the highest score loses
# 3. At the start of a round, passing occurs, following this pattern: Right, Left, Middle, None (Passing is designated by a Hand of 0)
# 4. The first hand begins with the player who has the 2 of Clubs, they must play that card first
#    On the first hand, if a player has no clubs, they CANNOT play a Heart of the Queen of Spades
# 5. A player may only start with hearts if hearts have been broken
#    Hearts can be broken when a player has no card matching the leading suit, or they only have hearts in their hand
# 6. Each heart in a trick a player collects is worth 1 point. The Queen of Spades is 13 points
# 7. If a player collects every heart AND the Queen of Spades, they instead gain 0 points and everyone else gains 26 points

#Create the list of cards
# 102 - 114: Clubs
# 202 - 214: Diamonds
# 302 - 314: Spades
# 402 - 414: Hearts
# Aces are high
DECK = [102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, #Clubs
        202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, #Diamonds
        302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, #Spades
        402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414] #Hearts
HAND_NUMBER = 0
ROUND_NUMBER = 1
PLAYERS = []
HAND_STARTING_PLAYER_NUMBER = 0
PLAYER_HAND_CARDS = [[], [], [], []]
PLAYER_POINTS = [0, 0, 0, 0]
PLAYER_TRICK_CARDS = [[], [], [], []]
HEARTS_BROKEN = False
CURRENT_PLAYED_HAND_CARDS = []
PASSED_CARDS = []
#DANGER: The GAME_OVER flag is used to indicate if the game needs to end immediately due to an unforseen error
GAME_OVER = False
#This array contains all the game states that will be written to a file once the game is over
GAME_STATE_ARRAY = []

RANDOM_AI_PATH = "./players/randomAI/mainAI.py"

####################################
def shuffle(cards):
  shuffledCards = []
  while len(cards) > 0:
    rand = random.randint(0, len(cards)-1)
    card = cards[rand]
    shuffledCards.append(card)
    del cards[rand]
  return shuffledCards
####################################
def callAI(aiPath):
  return subprocess.run(f'{aiPath} {gameState}', stdout=subprocess.PIPE).stdout.decode('utf-8')
####################################
def getCardSuit(card):
  #Dividing the card# by 100 and rounding gives us the suit: 1 - Clubs, 2 - Diamonds, 3 - Spades, 4 - Hearts
  return round(card/100)
####################################
def validatePlayedCard(handNumber, card, playedHandCards, playerCardsInHand, playerNumber, startingPlayerNumber):
  if handNumber == 1:
    #The starting player must play the 2 of Clubs
    #Other players may not play a heart of the Queen of Spades
    if playerNumber == startingPlayerNumber:
      return card == 102
    else:
      return getCardSuit(card) != 4 and card != 312 #We cannot play a Heart of the Queen of Spades
  else:
    playedCardSuit = getCardSuit(card)
    leadingSuit = getCardSuit(playedHandCards[0])
    if playedCardSuit == 4:
      #A heart was played, check if hearts are broken or if they have no cards of the leading suit
      if playerNumber == startingPlayerNumber and HEARTS_BROKEN: return True #If we are the starting player and hearts are broken, we can play a heart, this is valid
      else:
        if playedCardSuit == leadingSuit: return True #The played card followed the leading suit, this is valid
        for c in len(playerCardsInHand):
          if getCardSuit(c) == leadingSuit:
            return False #We have a card of the leading suit, we are not allowed to play the card we played. This is not valid
        return True #If we make it here, we don't have a card of the leading suit, whatever we played is valid
    elif playedCardSuit != leadingSuit:
      #Check if we have any cards of the leading suit or not
      for c in len(playerCardsInHand):
        if getCardSuit(c) == leadingSuit:
          return False #We have a card of the leading suit, we are not allowed to play the card we played. This is not valid
      return True #If we make it here, we don't have a card of the leading suit, whatever we played is valid
####################################

#Begin


#Get the players from the passed in parameter
PLAYER_NAMES = sys.argv[1].split("|")
WORKING_PATH = os.path.dirname(os.path.realpath(__file__))
PLAYER_MAINAI_PATH = []

for name in PLAYER_NAMES:
  parts = name.split(".")
  if parts[-1] == "py":
    PLAYER_MAINAI_PATH.append(f'python ./players/{name}')
  else:
    #Add more extensions here
    PLAYER_MAINAI_PATH.append(f'./players/{name}')

#Seed the random number generator
random.seed()
try:
  #Shuffle the deck
  DECK = shuffle(DECK)
  #Deal the cards
  for i in range(len(DECK)):
    card = DECK.pop(0)
    PLAYER_HAND_CARDS[i % 4].append(card)
    #Find the player with the 2 of Clubs
    if card == 102:
      HAND_STARTING_PLAYER_NUMBER = i % 4

  #While every player has less than 100 points
  while PLAYER_POINTS[0] < 100 and PLAYER_POINTS[1] < 100 and PLAYER_POINTS[2] < 100 and PLAYER_POINTS[3] < 100:
    #HAND_NUMBER = 0 means we are passing cards. Passing happens in a pattern of 4 rounds: Left, Right, Middle, None
    if ROUND_NUMBER % 4 < 3: HAND_NUMBER = 0
    else: HAND_NUMBER = 1

    #Each player's hand only has 13 cards, so there will only be 13 hands
    for i in len(13):
      #Loop through each player
      for i in len(4):
        #Generate the game state string
        gameState = f'{HAND_NUMBER}/{ROUND_NUMBER}/{i}/{HAND_STARTING_PLAYER_NUMBER}/{PLAYER_HAND_CARDS[i]}/{CURRENT_PLAYED_HAND_CARDS}/{",".join(PLAYER_POINTS)}/{",".join(PLAYER_TRICK_CARDS[0])}|{",".join(PLAYER_TRICK_CARDS[1])}|{",".join(PLAYER_TRICK_CARDS[2])}|{",".join(PLAYER_TRICK_CARDS[3])}'
        #                Hand#     /    Round# /Player#/    HandStartingPlayer#     /     CardsInHand      / CardsPlayedByOtherPlayers / TotalPlayerPointsInGame /   PlayerCardsTakenInRoundSoFar
        #Call each AI to pass cards
        if HAND_NUMBER == 0:
          #Get the passed cards
          cardsToPass = callAI(PLAYER_MAINAI_PATH[i])
          PASSED_CARDS[i].append(cardsToPass.split(","))
        else:
          playedCard = callAI(PLAYER_MAINAI_PATH[i])
          valid = validatePlayedCard(HAND_NUMBER, playedCard, CURRENT_PLAYED_HAND_CARDS, PLAYER_HAND_CARDS[i], i, HAND_STARTING_PLAYER_NUMBER)

          #If not valid, we need to replace the AI with the RandomAI
          if not valid: 
            #Replace the player with a RandomAI
            PLAYER_MAINAI_PATH[i] = RANDOM_AI_PATH
            playedCard = callAI(PLAYER_MAINAI_PATH[i])
            valid = validatePlayedCard(HAND_NUMBER, playedCard, CURRENT_PLAYED_HAND_CARDS, PLAYER_HAND_CARDS[i], i, HAND_STARTING_PLAYER_NUMBER)
            if not valid: 
              GAME_OVER = True
              break
          
          #Add the played card to the cards played this hand
          CURRENT_PLAYED_HAND_CARDS.append(playedCard)
          #Remove the played card from the players hand
          PLAYER_HAND_CARDS.remove(playedCard)
          #Add the current game state to the game state array
          GAME_STATE_ARRAY.append(gameState + '\n')
      if GAME_OVER:
        break
      
      if HAND_NUMBER == 0:
        match ROUND_NUMBER % 4:
          #We need to update each players cards in hand with their passed cards
          case 0: #Pass to the Left
            for i in len(4):
              for c in len(3):
                #Remove the cards this player passed
                PLAYER_HAND_CARDS[i].remove(PASSED_CARDS[i][c])
              for c in len(3):
                #Add the cards the player was passed
                PLAYER_HAND_CARDS[i].append(PASSED_CARDS[i-1][c])
          case 1: #Pass to the Right
            for i in len(4):
              for c in len(3):
                #Remove the cards this player passed
                PLAYER_HAND_CARDS[i].remove(PASSED_CARDS[i][c])
              if i == 3:
                #Need to give the 4th players cards to the first player
                for c in len(3):
                  #Add the cards the player was passed
                  PLAYER_HAND_CARDS[i].append(PASSED_CARDS[0][c])
              else:
                for c in len(3):
                  #Add the cards the player was passed
                  PLAYER_HAND_CARDS[i].append(PASSED_CARDS[i+1][c])
          case 2: #Pass to the middle
              for c in len(3):
                #Remove the cards this player passed
                PLAYER_HAND_CARDS[i].remove(PASSED_CARDS[i][c])
              if i < 2:
                for c in len(3):
                  #Add the cards the player was passed
                  PLAYER_HAND_CARDS[i].append(PASSED_CARDS[i+2][c])
              else:
                for c in len(3):
                  #Add the cards the player was passed
                  PLAYER_HAND_CARDS[i].append(PASSED_CARDS[i-2][c])
          case _: #No Passing
            #Nothing to do here
            PASSED_CARDS = []

        #Once passing is complete figure out who has the 2 of Clubs
        for i in len(4):
          if 102 in PLAYER_HAND_CARDS[i]:
            HAND_STARTING_PLAYER_NUMBER = i
            break
      else:
        #If we are not passing, we need to figure out who won the trick
        highCard = CURRENT_PLAYED_HAND_CARDS[0]
        winPlayer = 0
        leadSuit = getCardSuit(highCard)
        for c in len(CURRENT_PLAYED_HAND_CARDS):
          card = CURRENT_PLAYED_HAND_CARDS[c]
          cardSuit = getCardSuit(card)
          if cardSuit == leadSuit or cardSuit == 4:
            #If the played card is the same as the lead suit, or a heart was played
            #Compare the card values to see which is higher
            if card > highCard: 
              highCard = card
              winPlayer = c
        PLAYER_TRICK_CARDS[winPlayer].append(CURRENT_PLAYED_HAND_CARDS)
        #Reset the current played cards
        CURRENT_PLAYED_HAND_CARDS = []
      #Once each player has taken a turn, increase the hand number
      HAND_NUMBER += 1
    #At the end of each round, we need to add up all the points by each player
    shootTheMoonPlayer = -1
    for i in len(4):
      playerTricks = PLAYER_TRICK_CARDS[i]
      playerPointsThisRound = 0

      for trick in playerTricks:
        for card in trick:
          if getCardSuit(card) == 4: playerPointsThisRound += 1 #Any Heart
          if card == 312: playerPointsThisRound += 13 #The Queen of Spades
      if playerPointsThisRound == 26:
        #If someone got all Hearts and the Queen of Spades, they get 0 points and everyone else gets 26 points
        shootTheMoonPlayer = i
        playerPointsThisRound = 0
      else:
        if shootTheMoonPlayer >= 0:
          PLAYER_POINTS[i] += 26
        else:
          PLAYER_POINTS[i] += playerPointsThisRound

    #After each round, we need to increase the round number
    ROUND_NUMBER += 1

  if not GAME_OVER:
    sys.stdout.write(str("/".join(PLAYER_POINTS)))
  else:
    sys.stdout.write("////")

  #Write the game state array to a file
  f = open("./games/" + datetime.datetime.now() + ".txt", "w")
  f.writelines(GAME_STATE_ARRAY)
except:
  print("Error")