import sys #Needed to read command line parameters and output to the command line
import random #Needed to generate random numbers

#RANDOM AI
#Chooses a random card to play

#First lets read in the current state of the game
GAME_STATE = sys.argv[1]
#The 0th parameter is the name of the file
#The 1st parameter is the game state
# IE: sys.argv = ['mainAI.py', '1/2/3/...']

#Now we need to split the GAME_STATE by '/' to get all the information
parts = GAME_STATE.split("/")
HAND_NUMBER = int(parts[0])
ROUND_NUMBER = int(parts[1])
PLAYER_NUMBER = int(parts[2])
HAND_STARTING_PLAYER_NUMBER = int(parts[3])
CARDS_IN_HAND = list(map(int, parts[4].split(",")))
PLAYED_CARDS = list(map(int, parts[5].split(",")))
PLAYER_POINTS = list(map(int, parts[6].split(",")))
playerCardParts = parts[7].split("|")
#https://stackoverflow.com/questions/6429638/how-to-split-a-string-of-space-separated-numbers-into-integers

PLAYER_CARDS_WON = [] #This will be a 2D array
HEARTS_BROKEN = False

for playerCards in playerCardParts:
  cardsList = list(map(int, playerCards.split(",")))
  #While grabbing the player's cards, lets see if hearts have been broken
  if not HEARTS_BROKEN:
    #Only check to see if hearts have been broken if we haven't already determined if they've been broken
    for card in cardsList:
      if round(card/100) == 4:
        #Dividing the card# by 100 and rounding gives us the suit: 1 - Clubs, 2 - Diamonds, 3 - Spades, 4 - Hearts
        HEARTS_BROKEN = True
        #We don't need to keep checking cards now that we know hearts are broken
        break
  PLAYER_CARDS_WON.append(cardsList)

#Lets determine if we have cards other than hearts in our hand
ONLY_HEARTS_IN_HAND = True
for card in CARDS_IN_HAND:
  if round(card/100) < 4:
    #If we find a non-hearts, we don't need to keep looking
    ONLY_HEARTS_IN_HAND = False
    break

#The following functions are specific to the randomAI
####################################
def pickRandomCard(availabeCards):
  #Generate a random number
  randomNumber = random.randint(0, len(availabeCards)-1)
  #Store a reference to to the card's value
  card = availabeCards[randomNumber]
  #Remove the card from your hand once it has been picked
  del availabeCards[randomNumber]
  #Return the card we wish to play
  return card
####################################
def getCardSuit(card):
  #Dividing the card# by 100 and rounding gives us the suit: 1 - Clubs, 2 - Diamonds, 3 - Spades, 4 - Hearts
  return round(card/100)
####################################

#The following functions are the common functional logic that should be followed in your AI
####################################
# Define a function to print out the card we want to play, or the cards we are going to pass
def printCards(card):
  sys.stdout.write(str(card))
  sys.exit()
####################################
def passCards():
  #When passing cards, we need to pick 3 cards instead of 1 from our hand
  #Determine which direction we are passing
  passDirection = ROUND_NUMBER % 4
  #0: Pass Left 1: Pass Right 2: Pass Across 4: No Pass (On the fourth rounds, there will be no Hand 0, so don't worry about catching this)
  # The randomAI has no need to figure out which direction we are passing
  cardsToPass = []
  for i in range(3):
    #Get a random card to pass
    cardsToPass.append(pickRandomCard(CARDS_IN_HAND))
  return cardsToPass
####################################
def getCardToPlay():
  cardToPlay = 0
  if HAND_NUMBER == 1:
    #If it is the first hand, there are some special rules
    if HAND_STARTING_PLAYER_NUMBER != PLAYER_NUMBER:
      #If the starting player is not us, we cannot play a heart or the Queen of Spades
      while cardToPlay == 0:
        #Pick a card to play
        card = pickRandomCard(CARDS_IN_HAND)
        #Determine if the card is valid to be played on the first round
        if getCardSuit(card) < 4 and card != 312:
          # On the first round, we cannot play a heart `getCardSuit(card)` AND we cannot play the Queen of Spades `card != 312`
          cardToPlay = card
    else:
      #If we are the starting player, we must have the 2 of Clubs. We only have one option, to play that card
      #Lets do a sanity check to make sure we actually have the 2 of Clubs
      try:
        cardIndex = CARDS_IN_HAND.index(102)
        cardToPlay = CARDS_IN_HAND[cardIndex]
      except:
        #We do not have the 2 of Clubs
        cardToPlay = 999
  else:
    #On subsequent hands, the only rule is that we must follow the lead suit if possible
    if HAND_STARTING_PLAYER_NUMBER == PLAYER_NUMBER:
      #If we are the starting player, pick any card
      cardToPlay = pickRandomCard(CARDS_IN_HAND)
      #Wondering why there's no if check? A while loop checks the while condition first before running the body, so an if check is redundant
      # If hearts have been broken, we don't need to keep picking cards, we can lead with a heart
      while getCardSuit(cardToPlay) == 4 and not HEARTS_BROKEN and not ONLY_HEARTS_IN_HAND:
        #If hearts have not been broken, we cannot lead with a heart unless we only have hearts
        cardToPlay = pickRandomCard(CARDS_IN_HAND)
    else:
      leadSuit = getCardSuit(PLAYED_CARDS[0])
      #Let's find out which suit lead this round

      #Now lets find all cards we have that match the leading suit
      availableCards = []
      for card in CARDS_IN_HAND:
        if getCardSuit(card) == leadSuit:
          availableCards.append(card)
      
      if len(availableCards) > 0:
        #If we have a card that matches the lead suit, pick one to play
        cardToPlay = pickRandomCard(availableCards)
      else:
        #If we have no cards that match the lead suit, find a card to play
        # Since we have none of the lead suit, we can play anything even if hearts have not been broken
        cardToPlay = pickRandomCard(CARDS_IN_HAND)

  #Return the card we want to play
  return cardToPlay

#Lets seed our random number generator
random.seed()

#Now that we have all the information, lets figure out what to do
if HAND_NUMBER == 0: 
  cardsToPass = passCards()
  printCards(",".join(cardsToPass))
else:
  cardToPlay = getCardToPlay()
  printCards(cardToPlay)